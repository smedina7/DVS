/* proto_tree.cpp
 *
 * Wireshark - Network traffic analyzer
 * By Gerald Combs <gerald@wireshark.org>
 * Copyright 1998 Gerald Combs
 *
 * SPDX-License-Identifier: GPL-2.0-or-later
 */

#include <stdio.h>

#include <ui/qt/proto_tree.h>
#include <ui/qt/models/proto_tree_model.h>

#include <epan/ftypes/ftypes.h>
#include <epan/prefs.h>

#include <ui/qt/utils/color_utils.h>
#include <ui/qt/utils/variant_pointer.h>
#include <ui/qt/utils/wireshark_mime_data.h>
#include <ui/qt/widgets/drag_label.h>
#include <ui/qt/widgets/wireshark_file_dialog.h>
#include <ui/qt/show_packet_bytes_dialog.h>
#include <ui/qt/filter_action.h>
#include <ui/all_files_wildcard.h>
#include <ui/alert_box.h>
#include "wireshark_application.h"

#include <QApplication>
#include <QContextMenuEvent>
#include <QDesktopServices>
#include <QHeaderView>
#include <QItemSelectionModel>
#include <QScrollBar>
#include <QStack>
#include <QUrl>
#include <QClipboard>
#include <QWindow>
#include <QMessageBox>
#include <QJsonDocument>
#include <QJsonObject>

// To do:
// - Fix "apply as filter" behavior.

ProtoTree::ProtoTree(QWidget *parent, epan_dissect_t *edt_fixed) :
    QTreeView(parent),
    proto_tree_model_(new ProtoTreeModel(this)),
    decode_as_(NULL),
    column_resize_timer_(0),
    cap_file_(NULL),
    edt_(edt_fixed)
{
    setAccessibleName(tr("Packet details"));
    // Leave the uniformRowHeights property as-is (false) since items might
    // have multiple lines (e.g. packet comments). If this slows things down
    // too much we should add a custom delegate which handles SizeHintRole
    // similar to PacketListModel::data.
    setHeaderHidden(true);

#if !defined(Q_OS_WIN)
#if defined(Q_OS_MAC)
    QPalette default_pal = QApplication::palette();
    default_pal.setCurrentColorGroup(QPalette::Active);
    QColor hover_color = default_pal.highlight().color();
#else
    QColor hover_color = ColorUtils::alphaBlend(palette().window(), palette().highlight(), 0.5);
#endif

    setStyleSheet(QString(
        "QTreeView:item:hover {"
        "  background-color: %1;"
        "  color: palette(text);"
        "}").arg(hover_color.name(QColor::HexArgb)));
#endif

    // Shrink down to a small but nonzero size in the main splitter.
    int one_em = fontMetrics().height();
    setMinimumSize(one_em, one_em);

    setModel(proto_tree_model_);

    connect(this, SIGNAL(expanded(QModelIndex)), this, SLOT(syncExpanded(QModelIndex)));
    connect(this, SIGNAL(collapsed(QModelIndex)), this, SLOT(syncCollapsed(QModelIndex)));
    connect(this, SIGNAL(doubleClicked(QModelIndex)),
            this, SLOT(itemDoubleClicked(QModelIndex)));

    connect(&proto_prefs_menu_, SIGNAL(showProtocolPreferences(QString)),
            this, SIGNAL(showProtocolPreferences(QString)));
    connect(&proto_prefs_menu_, SIGNAL(editProtocolPreference(preference*,pref_module*)),
            this, SIGNAL(editProtocolPreference(preference*,pref_module*)));

    // resizeColumnToContents checks 1000 items by default. The user might
    // have scrolled to an area with a different width at this point.
    connect(verticalScrollBar(), SIGNAL(sliderReleased()),
            this, SLOT(updateContentWidth()));

    connect(wsApp, SIGNAL(appInitialized()), this, SLOT(connectToMainWindow()));

    viewport()->installEventFilter(this);
}

void ProtoTree::clear() {
    proto_tree_model_->setRootNode(NULL);
    updateContentWidth();
}

void ProtoTree::connectToMainWindow()
{
    if (wsApp->mainWindow())
    {
        connect(wsApp->mainWindow(), SIGNAL(fieldSelected(FieldInformation *)),
                this, SLOT(selectedFieldChanged(FieldInformation *)));
        connect(wsApp->mainWindow(), SIGNAL(frameSelected(int)),
                this, SLOT(selectedFrameChanged(int)));
    }
}

void ProtoTree::ctxCopyVisibleItems()
{
    bool selected_tree = false;

    QAction * send = qobject_cast<QAction *>(sender());
    if (send && send->property("selected_tree").isValid())
        selected_tree = true;

    QString clip = toString();
    if (selected_tree && selectionModel()->hasSelection())
        clip = toString(selectionModel()->selectedIndexes().first());

    if (clip.length() > 0)
        wsApp->clipboard()->setText(clip);
}

void ProtoTree::ctxCopyAsFilter()
{
    QModelIndex idx = selectionModel()->selectedIndexes().first();
    FieldInformation finfo(proto_tree_model_->protoNodeFromIndex(idx).protoNode());
    if (finfo.isValid())
    {
        epan_dissect_t *edt = cap_file_ ? cap_file_->edt : edt_;
        char *field_filter = proto_construct_match_selected_string(finfo.fieldInfo(), edt);
        QString filter(field_filter);
        wmem_free(Q_NULLPTR, field_filter);

        if (filter.length() > 0)
            wsApp->clipboard()->setText(filter);
    }
}

void ProtoTree::ctxCopySelectedInfo()
{
    int val = -1;
    QString clip;
    QAction * send = qobject_cast<QAction *>(sender());
    if (send && send->property("field_type").isValid())
        val = send->property("field_type").toInt();

    QModelIndex idx = selectionModel()->selectedIndexes().first();
    FieldInformation finfo(proto_tree_model_->protoNodeFromIndex(idx).protoNode());
    if (! finfo.isValid())
        return;

    switch (val)
    {
    case ProtoTree::Name:
        clip.append(finfo.headerInfo().abbreviation);
        break;

    case ProtoTree::Description:
        if (finfo.fieldInfo()->rep && strlen(finfo.fieldInfo()->rep->representation) > 0)
            clip.append(finfo.fieldInfo()->rep->representation);
        break;

    case ProtoTree::Value:
        {
            epan_dissect_t *edt = cap_file_ ? cap_file_->edt : edt_;
            gchar* field_str = get_node_field_value(finfo.fieldInfo(), edt);
            clip.append(field_str);
            g_free(field_str);
        }
        break;
    default:
        break;
    }

    if (clip.length() > 0)
        wsApp->clipboard()->setText(clip);
}

void ProtoTree::ctxOpenUrlWiki()
{
    QUrl url;
    bool is_field_reference = false;
    QAction * send = qobject_cast<QAction *>(sender());
    if (send && send->property("field_reference").isValid())
        is_field_reference = send->property("field_reference").toBool();
    QModelIndex idx = selectionModel()->selectedIndexes().first();
    FieldInformation finfo(proto_tree_model_->protoNodeFromIndex(idx).protoNode());

    const QString proto_abbrev = proto_registrar_get_abbrev(finfo.headerInfo().id);

    if (! is_field_reference)
    {
        int ret = QMessageBox::question(this, wsApp->windowTitleString(tr("Wiki Page for %1").arg(proto_abbrev)),
                                        tr("<p>The Wireshark Wiki is maintained by the community.</p>"
                                        "<p>The page you are about to load might be wonderful, "
                                        "incomplete, wrong, or nonexistent.</p>"
                                        "<p>Proceed to the wiki?</p>"),
                                        QMessageBox::Yes | QMessageBox::No, QMessageBox::Yes);

        if (ret != QMessageBox::Yes) return;

        url = QString("https://wiki.wireshark.org/Protocols/%1").arg(proto_abbrev);
    }
    else
    {
        url = QString("https://www.wireshark.org/docs/dfref/%1/%2")
                .arg(proto_abbrev[0])
                .arg(proto_abbrev);
    }

    QDesktopServices::openUrl(url);
}

void ProtoTree::contextMenuEvent(QContextMenuEvent *event)
{
    QModelIndex index = indexAt(event->pos());
    if (! index.isValid())
        return;

    // We're in a PacketDialog
    bool buildForDialog = false;
    if (! window()->findChild<QAction *>("actionViewExpandSubtrees"))
        buildForDialog = true;

    QMenu ctx_menu(this);

    QMenu *main_menu_item, *submenu;
    QAction *action;

     bool have_subtree = false;
    FieldInformation finfo(proto_tree_model_->protoNodeFromIndex(index).protoNode());
    field_info * fi = finfo.fieldInfo();
    bool is_selected = false;
    epan_dissect_t *edt = cap_file_ ? cap_file_->edt : edt_;

    if (cap_file_ && cap_file_->finfo_selected == fi)
        is_selected = true;
    else if (! window()->findChild<QAction *>("actionViewExpandSubtrees"))
        is_selected = true;

    if (is_selected)
    {
        if (fi && fi->tree_type != -1) {
            have_subtree = true;
        }
    }

    action = ctx_menu.addAction(tr("Expand Subtrees"), this, SLOT(expandSubtrees()));
    action->setEnabled(have_subtree);
    action = ctx_menu.addAction(tr("Collapse Subtrees"), this, SLOT(collapseSubtrees()));
    action->setEnabled(have_subtree);
    ctx_menu.addAction(tr("Expand All"), this, SLOT(expandAll()));
    ctx_menu.addAction(tr("Collapse All"), this, SLOT(collapseAll()));
    ctx_menu.addSeparator();

    if (! buildForDialog)
    {
        action = window()->findChild<QAction *>("actionAnalyzeCreateAColumn");
        ctx_menu.addAction(action);
        ctx_menu.addSeparator();
    }

    char * selectedfilter = proto_construct_match_selected_string(finfo.fieldInfo(), edt);
    bool can_match_selected = proto_can_match_selected(finfo.fieldInfo(), edt);
    ctx_menu.addMenu(FilterAction::createFilterMenu(FilterAction::ActionApply, selectedfilter, can_match_selected, &ctx_menu));
    ctx_menu.addMenu(FilterAction::createFilterMenu(FilterAction::ActionPrepare, selectedfilter, can_match_selected, &ctx_menu));
    if (selectedfilter)
        wmem_free(Q_NULLPTR, selectedfilter);

    if (! buildForDialog)
    {
        QMenu *main_conv_menu = window()->findChild<QMenu *>("menuConversationFilter");
        conv_menu_.setTitle(main_conv_menu->title());
        conv_menu_.clear();
        foreach (QAction *action, main_conv_menu->actions()) {
            conv_menu_.addAction(action);
        }

        ctx_menu.addMenu(&conv_menu_);

        colorize_menu_.setTitle(tr("Colorize with Filter"));
        ctx_menu.addMenu(&colorize_menu_);

        main_menu_item = window()->findChild<QMenu *>("menuFollow");
        submenu = new QMenu(main_menu_item->title(), &ctx_menu);
        ctx_menu.addMenu(submenu);
        submenu->addAction(window()->findChild<QAction *>("actionAnalyzeFollowTCPStream"));
        submenu->addAction(window()->findChild<QAction *>("actionAnalyzeFollowUDPStream"));
        submenu->addAction(window()->findChild<QAction *>("actionAnalyzeFollowTLSStream"));
        submenu->addAction(window()->findChild<QAction *>("actionAnalyzeFollowHTTPStream"));
        submenu->addAction(window()->findChild<QAction *>("actionAnalyzeFollowHTTP2Stream"));
        submenu->addAction(window()->findChild<QAction *>("actionAnalyzeFollowQUICStream"));
        ctx_menu.addSeparator();
    }

    submenu = ctx_menu.addMenu(tr("Copy"));
    submenu->addAction(tr("All Visible Items"), this, SLOT(ctxCopyVisibleItems()));
    action = submenu->addAction(tr("All Visible Selected Tree Items"), this, SLOT(ctxCopyVisibleItems()));
    action->setProperty("selected_tree", qVariantFromValue(true));
    action = submenu->addAction(tr("Description"), this, SLOT(ctxCopySelectedInfo()));
    action->setProperty("field_type", ProtoTree::Description);
    action = submenu->addAction(tr("Field Name"), this, SLOT(ctxCopySelectedInfo()));
    action->setProperty("field_type", ProtoTree::Name);
    action = submenu->addAction(tr("Value"), this, SLOT(ctxCopySelectedInfo()));
    action->setProperty("field_type", ProtoTree::Value);
    submenu->addSeparator();
    submenu->addAction(tr("As Filter"), this, SLOT(ctxCopyAsFilter()));
    QActionGroup * copyEntries = DataPrinter::copyActions(this, &finfo);
    submenu->addActions(copyEntries->actions());
    ctx_menu.addSeparator();

    if (! buildForDialog)
    {
        action = window()->findChild<QAction *>("actionAnalyzeShowPacketBytes");
        ctx_menu.addAction(action);
        action = window()->findChild<QAction *>("actionFileExportPacketBytes");
        ctx_menu.addAction(action);

        ctx_menu.addSeparator();
    }

    ctx_menu.addAction(tr("Wiki Protocol Page"), this, SLOT(ctxOpenUrlWiki()));
    action = ctx_menu.addAction(tr("Filter Field Reference"), this, SLOT(ctxOpenUrlWiki()));
    action->setProperty("field_reference", qVariantFromValue(true));
    ctx_menu.addMenu(&proto_prefs_menu_);
    ctx_menu.addSeparator();
    decode_as_ = window()->findChild<QAction *>("actionAnalyzeDecodeAs");
    ctx_menu.addAction(decode_as_);

    if (! buildForDialog)
    {
        ctx_menu.addAction(window()->findChild<QAction *>("actionGoGoToLinkedPacket"));
        ctx_menu.addAction(window()->findChild<QAction *>("actionContextShowLinkedPacketInNewWindow"));

        // The "text only" header field will not give preferences for the selected protocol.
        // Use parent in this case.
        proto_node *node = proto_tree_model_->protoNodeFromIndex(index).protoNode();
        while (node && node->finfo && node->finfo->hfinfo && node->finfo->hfinfo->id == hf_text_only)
            node = node->parent;

        FieldInformation pref_finfo(node);
        proto_prefs_menu_.setModule(pref_finfo.moduleName());

        decode_as_->setData(QVariant::fromValue(true));
    }

    ctx_menu.exec(event->globalPos());

    if (! buildForDialog)
        decode_as_->setData(QVariant());
}

void ProtoTree::timerEvent(QTimerEvent *event)
{
    if (event->timerId() == column_resize_timer_) {
        killTimer(column_resize_timer_);
        column_resize_timer_ = 0;
        resizeColumnToContents(0);
    } else {
        QTreeView::timerEvent(event);
    }
}

// resizeColumnToContents checks 1000 items by default. The user might
// have scrolled to an area with a different width at this point.
void ProtoTree::keyReleaseEvent(QKeyEvent *event)
{
    if (event->isAutoRepeat()) return;

    switch(event->key()) {
        case Qt::Key_Up:
        case Qt::Key_Down:
        case Qt::Key_PageUp:
        case Qt::Key_PageDown:
        case Qt::Key_Home:
        case Qt::Key_End:
            updateContentWidth();
            break;
        default:
            break;
    }
}

void ProtoTree::updateContentWidth()
{
    if (column_resize_timer_ == 0) {
        column_resize_timer_ = startTimer(0);
    }
}

void ProtoTree::setMonospaceFont(const QFont &mono_font)
{
    mono_font_ = mono_font;
    setFont(mono_font_);
    update();
}

void ProtoTree::foreachTreeNode(proto_node *node, gpointer proto_tree_ptr)
{
    ProtoTree *tree_view = static_cast<ProtoTree *>(proto_tree_ptr);
    ProtoTreeModel *model = qobject_cast<ProtoTreeModel *>(tree_view->model());
    if (!tree_view || !model) {
        return;
    }

    // Expanded state
    if (tree_expanded(node->finfo->tree_type)) {
        ProtoNode expand_node = ProtoNode(node);
        tree_view->expand(model->indexFromProtoNode(expand_node));
    }

    // Related frames
    if (node->finfo->hfinfo->type == FT_FRAMENUM) {
        ft_framenum_type_t framenum_type = (ft_framenum_type_t)GPOINTER_TO_INT(node->finfo->hfinfo->strings);
        tree_view->emitRelatedFrame(node->finfo->value.value.uinteger, framenum_type);
    }

    proto_tree_children_foreach(node, foreachTreeNode, proto_tree_ptr);
}

// We track item expansion using proto.c:tree_is_expanded. QTreeView
// tracks it using QTreeViewPrivate::expandedIndexes. When we're handed
// a new tree, clear expandedIndexes and repopulate it by walking the
// tree and calling QTreeView::expand above.
void ProtoTree::setRootNode(proto_node *root_node) {
    setFont(mono_font_);
    reset(); // clears expandedIndexes.
    proto_tree_model_->setRootNode(root_node);

    disconnect(this, SIGNAL(expanded(QModelIndex)), this, SLOT(syncExpanded(QModelIndex)));
    proto_tree_children_foreach(root_node, foreachTreeNode, this);
    connect(this, SIGNAL(expanded(QModelIndex)), this, SLOT(syncExpanded(QModelIndex)));

    updateContentWidth();
}

void ProtoTree::emitRelatedFrame(int related_frame, ft_framenum_type_t framenum_type)
{
    emit relatedFrame(related_frame, framenum_type);
}

void ProtoTree::autoScrollTo(const QModelIndex &index)
{
    selectionModel()->setCurrentIndex(index, QItemSelectionModel::ClearAndSelect);
    if (!index.isValid()) {
        return;
    }

    // ensure item is visible (expanding its parents as needed).
    scrollTo(index);
}

// XXX We select the first match, which might not be the desired item.
void ProtoTree::goToHfid(int hfid)
{
    QModelIndex index = proto_tree_model_->findFirstHfid(hfid);
    autoScrollTo(index);
}

void ProtoTree::selectionChanged(const QItemSelection &selected, const QItemSelection &deselected)
{
    QTreeView::selectionChanged(selected, deselected);
    if (selected.isEmpty()) {
        emit fieldSelected(0);
        return;
    }

    QModelIndex index = selected.indexes().first();
    saveSelectedField(index);

    // Find and highlight the protocol bytes. select above won't call
    // selectionChanged if the current and selected indexes are the same
    // so we do this here.
    FieldInformation finfo(proto_tree_model_->protoNodeFromIndex(index).protoNode(), this);
    if (finfo.isValid()) {
        QModelIndex parent = index;
        while (parent.isValid() && parent.parent().isValid()) {
            parent = parent.parent();
        }
        if (parent.isValid()) {
            FieldInformation parent_finfo(proto_tree_model_->protoNodeFromIndex(parent).protoNode());
            finfo.setParentField(parent_finfo.fieldInfo());
        }
        emit fieldSelected(&finfo);
    }
}

void ProtoTree::syncExpanded(const QModelIndex &index) {
    FieldInformation finfo(proto_tree_model_->protoNodeFromIndex(index).protoNode());
    if (!finfo.isValid()) return;

    /*
     * Nodes with "finfo->tree_type" of -1 have no ett_ value, and
     * are thus presumably leaf nodes and cannot be expanded.
     */
    if (finfo.treeType() != -1) {
        tree_expanded_set(finfo.treeType(), TRUE);
    }
}

void ProtoTree::syncCollapsed(const QModelIndex &index) {
    FieldInformation finfo(proto_tree_model_->protoNodeFromIndex(index).protoNode());
    if (!finfo.isValid()) return;

    /*
     * Nodes with "finfo->tree_type" of -1 have no ett_ value, and
     * are thus presumably leaf nodes and cannot be collapsed.
     */
    if (finfo.treeType() != -1) {
        tree_expanded_set(finfo.treeType(), FALSE);
    }
}

void ProtoTree::expandSubtrees()
{
    if (!selectionModel()->hasSelection()) return;

    QStack<QModelIndex> index_stack;
    index_stack.push(selectionModel()->selectedIndexes().first());

    while (!index_stack.isEmpty()) {
        QModelIndex index = index_stack.pop();
        expand(index);
        int row_count = proto_tree_model_->rowCount(index);
        for (int row = row_count - 1; row >= 0; row--) {
            QModelIndex child = proto_tree_model_->index(row, 0, index);
            if (proto_tree_model_->hasChildren(child)) {
                index_stack.push(child);
            }
        }
    }

    updateContentWidth();
}

void ProtoTree::collapseSubtrees()
{
    if (!selectionModel()->hasSelection()) return;

    QStack<QModelIndex> index_stack;
    index_stack.push(selectionModel()->selectedIndexes().first());

    while (!index_stack.isEmpty()) {
        QModelIndex index = index_stack.pop();
        collapse(index);
        int row_count = proto_tree_model_->rowCount(index);
        for (int row = row_count - 1; row >= 0; row--) {
            QModelIndex child = proto_tree_model_->index(row, 0, index);
            if (proto_tree_model_->hasChildren(child)) {
                index_stack.push(child);
            }
        }
    }

    updateContentWidth();
}

void ProtoTree::expandAll()
{
    for (int i = 0; i < num_tree_types; i++) {
        tree_expanded_set(i, TRUE);
    }
    QTreeView::expandAll();
    updateContentWidth();
}

void ProtoTree::collapseAll()
{
    for (int i = 0; i < num_tree_types; i++) {
        tree_expanded_set(i, FALSE);
    }
    QTreeView::collapseAll();
    updateContentWidth();
}

void ProtoTree::itemDoubleClicked(const QModelIndex &index) {
    FieldInformation finfo(proto_tree_model_->protoNodeFromIndex(index).protoNode());
    if (!finfo.isValid()) return;

    if (finfo.headerInfo().type == FT_FRAMENUM) {
        if (QApplication::queryKeyboardModifiers() & Qt::ShiftModifier) {
            emit openPacketInNewWindow(true);
        } else {
            emit goToPacket(finfo.fieldInfo()->value.value.uinteger);
        }
    } else {
        QString url = finfo.url();
        if (!url.isEmpty()) {
            QDesktopServices::openUrl(QUrl(url));
        }
    }
}

void ProtoTree::selectedFrameChanged(int frameNum)
{
    if (frameNum < 0)
        proto_tree_model_->setRootNode(Q_NULLPTR);
}

// Select a field and bring it into view. Intended to be called by external
// components (such as the byte view).
void ProtoTree::selectedFieldChanged(FieldInformation *finfo)
{
    if (finfo && finfo->parent() == this) {
        // We only want inbound signals.
        return;
    }

    QModelIndex index = proto_tree_model_->findFieldInformation(finfo);
    setUpdatesEnabled(false);
    // The new finfo might match the current index. Clear our selection
    // so that we force a fresh item selection, so that fieldSelected
    // will in turn be emitted.
    selectionModel()->clearSelection();
    autoScrollTo(index);
    setUpdatesEnabled(true);
}

// Remember the currently focussed field based on:
// - current hf_id (obviously)
// - parent items (to avoid selecting a text item in a different tree)
// - the row of each item
void ProtoTree::saveSelectedField(QModelIndex &index)
{
    selected_hfid_path_.clear();
    QModelIndex save_index = index;
    while (save_index.isValid()) {
        FieldInformation finfo(proto_tree_model_->protoNodeFromIndex(save_index).protoNode());
        if (!finfo.isValid()) break;
        selected_hfid_path_.prepend(QPair<int,int>(save_index.row(), finfo.headerInfo().id));
        save_index = save_index.parent();
    }
}

// Try to focus a tree item which was previously also visible
void ProtoTree::restoreSelectedField()
{
    if (selected_hfid_path_.isEmpty()) return;

    QModelIndex cur_index = QModelIndex();
    QPair<int,int> path_entry;
    foreach (path_entry, selected_hfid_path_) {
        int row = path_entry.first;
        int hf_id = path_entry.second;
        cur_index = proto_tree_model_->index(row, 0, cur_index);
        FieldInformation finfo(proto_tree_model_->protoNodeFromIndex(cur_index).protoNode());
        if (!finfo.isValid() || finfo.headerInfo().id != hf_id) {
            // Did not find the selected hfid path in the selected packet
            cur_index = QModelIndex();
            emit fieldSelected(0);
            break;
        }
    }

    autoScrollTo(cur_index);
}

QString ProtoTree::traverseTree(const QModelIndex & travTree, int identLevel) const
{
    QString result = "";

    if (travTree.isValid())
    {
        result.append(QString("    ").repeated(identLevel));
        result.append(travTree.data().toString());
        result.append("\n");

        /* if the element is expanded, we traverse one level down */
        if (isExpanded(travTree))
        {
            int children = proto_tree_model_->rowCount(travTree);
            identLevel++;
            for (int child = 0; child < children; child++)
                result += traverseTree(proto_tree_model_->index(child, 0, travTree), identLevel);
        }
    }

    return result;
}

QString ProtoTree::toString(const QModelIndex &start_idx) const
{
    QString tree_string = "";
    if (start_idx.isValid())
        tree_string = traverseTree(start_idx, 0);
    else
    {
        int children = proto_tree_model_->rowCount();
        for (int child = 0; child < children; child++)
            tree_string += traverseTree(proto_tree_model_->index(child, 0, QModelIndex()), 0);
    }

    return tree_string;
}

//Retrieve keypressess added to packet information from
//custom dissector keypresses.lua
QString ProtoTree::getKeypresses() const {
    QString keypressess = QString("");
    std::string search_pattern = "Log Data: ";
    std::string log_data;
    QModelIndex travTree;
    QModelIndex kpData;
    int children = proto_tree_model_->rowCount();

    for (int child = 0; child < children; child++ ) {
        travTree = proto_tree_model_->index(child, 0, QModelIndex());
        if (travTree.isValid()) {
            if(travTree.data().toString() == "keypresses Log") {
                log_data = proto_tree_model_->index(1, 0, travTree).data().toString().toStdString();
                keypressess.append(QString(log_data.substr(search_pattern.length() + 1, log_data.length() - search_pattern.length() + 1).c_str()) + "\n");
            }
        }
    }

    return keypressess;
}

//Retrieve systemcalls added to packet information from
//custom dissector systemcalls.lua
QString ProtoTree::getSystemcalls() const {
    QString systemcalls = QString("");
    std::string search_pattern = "Log Data: ";
    std::string log_data;
    QModelIndex travTree;
    QModelIndex scData;
    int children = proto_tree_model_->rowCount();

    for (int child = 0; child < children; child++ ) {
        travTree = proto_tree_model_->index(child, 0, QModelIndex());
        if (travTree.isValid()) {
            if(travTree.data().toString() == "systemcalls Log") {
                log_data = proto_tree_model_->index(1, 0, travTree).data().toString().toStdString();
                systemcalls.append(QString(log_data.substr(search_pattern.length() + 1, log_data.length() - search_pattern.length() + 1).c_str()) + "\n");
            }
        }
    }

    return systemcalls;
}


//Retrieve suricata IDS alerts added to packet information from
//custom dissector suricataalerts.lua
QString ProtoTree::getSuricataAlerts() const {
    QString suricata = QString("");
    std::string search_pattern = "Log Data: ";
    std::string log_data;
    QModelIndex travTree;
    QModelIndex kpData;
    int children = proto_tree_model_->rowCount();

    for (int child = 0; child < children; child++ ) {
        travTree = proto_tree_model_->index(child, 0, QModelIndex());
        if (travTree.isValid()) {
            if(travTree.data().toString() == "suricata Log") {
                log_data = proto_tree_model_->index(1, 0, travTree).data().toString().toStdString();
                suricata.append(QString(log_data.substr(search_pattern.length() + 1, log_data.length() - search_pattern.length() + 1).c_str()) + "\n");
            }
        }
    }

    return suricata;
}


void ProtoTree::setCaptureFile(capture_file *cf)
{
    // For use by the main view, set the capture file which will later have a
    // dissection (EDT) ready.
    // The packet dialog sets a fixed EDT context and MUST NOT use this.
    Q_ASSERT(edt_ == NULL);
    cap_file_ = cf;
}

bool ProtoTree::eventFilter(QObject * obj, QEvent * event)
{
    if (event->type() != QEvent::MouseButtonPress && event->type() != QEvent::MouseMove)
        return QTreeView::eventFilter(obj, event);

    /* Mouse was over scrollbar, ignoring */
    if (qobject_cast<QScrollBar *>(obj))
        return QTreeView::eventFilter(obj, event);

    if (event->type() == QEvent::MouseButtonPress)
    {
        QMouseEvent * ev = (QMouseEvent *)event;

        if (ev->buttons() & Qt::LeftButton)
            drag_start_position_ = ev->pos();
    }
    else if (event->type() == QEvent::MouseMove)
    {
        QMouseEvent * ev = (QMouseEvent *)event;

        if ((ev->buttons() & Qt::LeftButton) && (ev->pos() - drag_start_position_).manhattanLength()
                 > QApplication::startDragDistance())
        {
            QModelIndex idx = indexAt(drag_start_position_);
            FieldInformation finfo(proto_tree_model_->protoNodeFromIndex(idx).protoNode());
            if (finfo.isValid())
            {
                /* Hack to prevent QItemSelection taking the item which has been dragged over at start
                 * of drag-drop operation. selectionModel()->blockSignals could have done the trick, but
                 * it does not take in a QTreeWidget (maybe View) */
                emit fieldSelected(&finfo);
                selectionModel()->select(idx, QItemSelectionModel::ClearAndSelect);

                epan_dissect_t *edt = cap_file_ ? cap_file_->edt : edt_;
                char *field_filter = proto_construct_match_selected_string(finfo.fieldInfo(), edt);
                QString filter(field_filter);
                wmem_free(NULL, field_filter);

                if (filter.length() > 0)
                {
                    QJsonObject filterData;
                    filterData["filter"] = filter;
                    filterData["name"] = finfo.headerInfo().abbreviation;
                    filterData["description"] = finfo.headerInfo().name;
                    QMimeData * mimeData = new QMimeData();

                    mimeData->setData(WiresharkMimeData::DisplayFilterMimeType, QJsonDocument(filterData).toJson());
                    mimeData->setText(toString(idx));

                    QDrag * drag = new QDrag(this);
                    drag->setMimeData(mimeData);

                    QString lblTxt = QString("%1\n%2").arg(finfo.headerInfo().name, filter);

                    DragLabel * content = new DragLabel(lblTxt, this);

                    qreal dpr = window()->windowHandle()->devicePixelRatio();
                    QPixmap pixmap(content->size() * dpr);
                    pixmap.setDevicePixelRatio(dpr);
                    content->render(&pixmap);
                    drag->setPixmap(pixmap);

                    drag->exec(Qt::CopyAction);

                    return true;
                }
            }
        }
    }

    return QTreeView::eventFilter(obj, event);
}

QModelIndex ProtoTree::moveCursor(QAbstractItemView::CursorAction cursorAction, Qt::KeyboardModifiers modifiers)
{
    if (cursorAction == MoveLeft && selectionModel()->hasSelection()) {
        QModelIndex cur_idx = selectionModel()->selectedIndexes().first();
        QModelIndex parent = cur_idx.parent();
        if (!isExpanded(cur_idx) && parent.isValid() && parent != rootIndex()) {
            return parent;
        }
    }
    return QTreeView::moveCursor(cursorAction, modifiers);
}

/*
 * Editor modelines
 *
 * Local Variables:
 * c-basic-offset: 4
 * tab-width: 8
 * indent-tabs-mode: nil
 * End:
 *
 * ex: set shiftwidth=4 tabstop=8 expandtab:
 * :indentSize=4:tabSize=8:noTabs=true:
 */

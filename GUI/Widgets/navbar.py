import dash_bootstrap_components as dbc

def Navbar():
   navbar = dbc.NavbarSimple(
      children=[
         dbc.NavItem(dbc.NavLink("Keypresses", href="/keypresses")),
         dbc.NavItem(dbc.NavLink("MouseClicks", href="/mouseclicks")),
         dbc.NavItem(dbc.NavLink("SystemCalls", href="/systemcalls")),
         dbc.NavItem(dbc.NavLink("Throughput", href="/throughput")),
      ]
   )
   return navbar

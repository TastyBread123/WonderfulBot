from . import on_text, on_member_join

event_routers = [on_text.router, on_member_join.router]
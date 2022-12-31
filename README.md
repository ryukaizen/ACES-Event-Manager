# TODOs
- Import option
- Reset button in content configuration
  1. Ability to merge saved content and generated date, time and venue values

# Reminder:

Uncomment the following line in app.py to enable GuestDashboard (currently it's launching AdminDashboard)

`#command=lambda: [widget.destroy() for widget in self.winfo_children()] + [GuestDashboard(self)]`

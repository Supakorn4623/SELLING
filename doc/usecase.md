**Use Case Diagram for SELLING project**

This folder contains `usecase.puml` — a PlantUML source file describing the main actors and use cases.

Actors (based on the project structure and templates):
- Shop Owner
- Salesperson

Main use cases:
- Login
- Manage Employees (create / edit / delete / list)
- View Dashboard
- View Reports (sales, stock)
- Product Management
- Add Stock
- Move To Shelf
- Sell Product (includes Process Payment, Generate Receipt)

How to render the diagram

1) Using the PlantUML jar (requires Java):

```powershell
# from project root
java -jar plantuml.jar doc\usecase.puml
```

2) Using VS Code PlantUML extension: open `doc/usecase.puml`, then preview (Alt+D / PlantUML: Preview).

3) Use the online PlantUML server: paste the contents into https://www.planttext.com/ or https://plantuml.com/ to render.

Notes
- I derived actors and use cases from `shopowner/` and `shopsales/` templates (dashboards, employee management, sales, stock management).
- If you want a modified diagram (more actors, or separate use-cases split), tell me which parts to expand and I will update the `.puml`.

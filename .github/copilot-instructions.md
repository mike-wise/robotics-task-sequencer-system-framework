### 🧠 Copilot Instructions for C# Development

  #### ✅ **General Principles**
  - Follow **SOLID** principles.
  - Write **readable**, **maintainable**, and **testable** code.
  - Avoid over-engineering and premature optimization.
  - Use **meaningful names** for variables, methods, and classes.

  ---

  #### 📆 **Project Structure**
  - Every **class**, **interface**, and **enum** should be in its **own file**.
  - File names should match the primary type they contain.
  - Group related files by feature or domain, not by type (e.g., `/Orders/OrderService.cs` instead of `/Services/OrderService.cs`).

  ---

  #### ✂️ **File Size Guidelines**
  - Try to keep files **under 300 lines** of code.
  - Break up large classes using:
    - Partial classes (if justified)
    - Smaller helper classes
    - Extension methods
    - Composition over inheritance

  ---

  #### 🚫 **Avoid These Code Smells**
  - **God Classes**: Classes that know too much or do too much.
  - **Long Methods**: Split into smaller methods (ideally ≤ 30 lines).
  - **Primitive Obsession**: Encapsulate primitives in value objects.
  - **Duplicated Code**: DRY (Don’t Repeat Yourself).
  - **Low Cohesion**: Each class should have a single responsibility.
  - **Feature Envy**: Methods that heavily depend on other classes’ internals.
  - **Shotgun Surgery**: A change requires modifying many classes/files.

  ---

  #### 🧪 **Testing**
  - Favor **dependency injection** to simplify testing.
  - Write **unit tests** for core logic.
  - Ensure code is **testable** by avoiding static classes and tight coupling.

  ---

  #### 🔧 **Code Style & Conventions**
  - Follow **.NET naming conventions**:
    - `PascalCase` for classes, properties, and methods.
    - `camelCase` for private fields and method parameters.
  - Use `var` when the type is **obvious**, otherwise be explicit.
  - Add **XML doc comments** for public methods and classes.
  - Use **expression-bodied members** for simple properties or methods.

  ---

  #### 🧼 **Maintainability Tips**
  - Use **regions** sparingly, only to logically group code.
  - Comment **why**, not **what**.
  - Prefer **immutable data** where appropriate.
  - Avoid magic strings/numbers – use constants or enums.
  - Apply the **Single Level of Abstraction** principle in methods.
  - Review and refactor regularly to manage **technical debt**.
  - Use **code analyzers and linters** (e.g., Roslyn analyzers) to enforce style and rules.

  ---

  #### 🔜 **Team-Specific Practices**
  - Use **Serilog** for consistent structured logging.
  - Errors must be handled using try-catch blocks with meaningful logs, not swallowed silently.
  - Prefer `async/await` patterns for I/O-bound operations.
  - Every pull request must:
    - Pass CI checks.
    - Include at least one **peer review**.
    - Contain **meaningful commit messages**.
  - Maintain a shared **stylecop.json** and `.editorconfig` to enforce consistent formatting.
  - Use **interfaces** for abstractions and define them close to their domain.
  - All new features must include **unit tests and documentation**.

  ---

  #### ⚖️ **Architectural Guidance**
  - Follow **Clean Architecture** or **Onion Architecture** layering principles.
  - Use **MediatR** for separation of concerns in CQRS-based applications.
  - Use DTOs for API boundaries and keep domain models internal.
  - Avoid tight coupling between layers. Use interfaces and dependency inversion.  - All external services (e.g., APIs, databases) should be accessed via a dedicated adapter or service class.

  ---

### 🐍 Copilot Instructions for Python Development

#### ✅ **General Principles**
- Follow **PEP 8** style guide for Python code.
- Write **readable**, **maintainable**, and **testable** code.
- Embrace Python's philosophy: "Simple is better than complex."
- Use **meaningful names** for variables, functions, and classes.
- Prefer **explicit over implicit** - code should be self-documenting.

---

#### 📆 **Project Structure**
- Use **packages and modules** to organize code logically.
- Follow standard Python project structure:
  ```
  project/
  ├── src/
  │   └── package_name/
  │       ├── __init__.py
  │       ├── main.py
  │       └── modules/
  ├── tests/
  ├── docs/
  ├── requirements.txt
  ├── setup.py (or pyproject.toml)
  └── README.md
  ```
- Group related functionality in modules, not by type.
- Use `__init__.py` files to control package imports.

---

#### ✂️ **File Size Guidelines**
- Keep modules **under 500 lines** of code.
- Break up large modules using:
  - Submodules and packages
  - Separate classes into different files
  - Extract utility functions to helper modules
  - Use composition and delegation

---

#### 🚫 **Avoid These Code Smells**
- **God Classes/Functions**: Functions/classes that do too much.
- **Long Functions**: Split into smaller functions (ideally ≤ 20-30 lines).
- **Nested Complexity**: Avoid deep nesting; use early returns and guard clauses.
- **Duplicated Code**: Follow DRY principles.
- **Magic Numbers/Strings**: Use constants or configuration files.
- **Mutable Default Arguments**: Use `None` and initialize inside the function.
- **Bare `except` clauses**: Always specify exception types.

---

#### 🧪 **Testing**
- Use **pytest** as the primary testing framework.
- Write **unit tests** for all functions and classes.
- Use **dependency injection** or **mocking** to isolate units under test.
- Follow **AAA pattern**: Arrange, Act, Assert.
- Use **fixtures** for test setup and teardown.
- Aim for **high test coverage** (80%+ line coverage).

---

#### 🔧 **Code Style & Conventions**
- Follow **PEP 8** naming conventions:
  - `snake_case` for functions, variables, and module names.
  - `PascalCase` for class names.
  - `UPPER_CASE` for constants.
- Use **type hints** for function parameters and return values.
- Write **docstrings** for all public functions, classes, and modules.
- Use **f-strings** for string formatting (Python 3.6+).
- Prefer **list/dict comprehensions** over loops when appropriate.

---

#### 🧼 **Maintainability Tips**
- Use **virtual environments** (venv, conda, pipenv) for dependency isolation.
- Pin dependencies in `requirements.txt` with specific versions.
- Use **dataclasses** or **pydantic** for structured data.
- Prefer **pathlib** over `os.path` for file operations.
- Use **context managers** (`with` statements) for resource management.
- Apply **SOLID principles** adapted for Python.
- Use **linters** (flake8, pylint) and **formatters** (black, autopep8).

---

#### 🔜 **Team-Specific Practices**
- Use **logging module** for consistent structured logging.
- Handle exceptions gracefully with specific exception types.
- Prefer **async/await** for I/O-bound operations when using async frameworks.
- Every pull request must:
  - Pass CI checks (tests, linting, type checking).
  - Include at least one **peer review**.
  - Contain **meaningful commit messages**.
- Maintain **pyproject.toml** or **setup.cfg** for project configuration.
- Use **interfaces** (abstract base classes) for abstractions.
- All new features must include **unit tests and documentation**.

---

#### ⚖️ **Architectural Guidance**
- Follow **Clean Architecture** or **Hexagonal Architecture** principles.
- Use **dependency injection** containers when building larger applications.
- Separate **business logic** from **infrastructure concerns**.
- Use **DTOs/Models** for API boundaries and data transfer.
- Avoid tight coupling between modules. Use dependency inversion.
- Consider using **design patterns** appropriate for Python (Factory, Strategy, Observer).
- For web applications, consider frameworks like **FastAPI**, **Django**, or **Flask**.
- Use **SQLAlchemy** or similar ORMs for database operations.

---

## Guidelines for Creating or Updating a Plan
- When creating a plan, organize it into numbered phases (e.g., "Phase 1: Setup Dependencies")
- Break down each phase into specific tasks with numeric identifiers (e.g., "Task 1.1: Add Dependencies")
- Use a consistent format for each task, including a description, expected outcome, and any dependencies or prerequisites
- Include a section for "Success Criteria" at the end of the plan to define when the implementation is complete
- Use markdown formatting for clarity and readability
- Use headings, bullet points, and code blocks as needed to enhance readability
- Include links to relevant documentation or resources where applicable
- Map out the Phases and tasks to an agile process that could live in a Kanban board or similar
- Add a field to track related issues even if in different phases or tasks. This can be a simple list of issue numbers or links to the issues in your issue tracker
- Please only create one document per plan
- Mark phases and tasks as `- [ ]` while not complete and `- [x]` once completed
- End the plan with success criteria that define when the implementation is complete
- Plans and architectures that you produce should go under `docs/plans`
- Use a consistent naming convention `YYYYMMDD-<short-description>.md` for plan files

## Guidelines for Implementing a Plan
- Code you write should go under `src`
- When coding you need to follow the plan and check off phases and tasks as they are completed
- Make sure to follow dependencies and prerequisites as outlined in the plan
- As you complete a task, update the plan by marking that task as complete before you begin the next task
- As you complete a phase, update the plan by marking that phase as complete before you begin the next phase
- Tasks that involve tests should not be marked complete until the tests pass.
- When you complete implementation for a plan phase, create an implementation note entry and summarize the completed work. Use one note file per plan, in `docs/notes` with naming convention `<plan-file-name>-note.md`
   - Link to the plan file in the note entry
   - Phase name
   - Timestamp and name of person who made the change
   - Major files added, updated, removed
   - Major features added, updated, removed
   - Use of patterns, abstractions, data structures, algorithms, etc.
   - Governing design principles


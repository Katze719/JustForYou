classDiagram
    %% Hauptklassen des Systems
    class MainWindow {
        +start()
        +loadModule(module: Module)
        +displayResults(results: List)
    }

    class Module {
        <<interface>>
        +execute(params: List) : Result
        +getInputFields() : List
    }

    class ArithmeticModule {
        +execute(params: List) : Result
    }

    class PercentageModule {
        +execute(params: List) : Result
        +%add()
        +%remove()
        +%calculate()
    }

    class CreditModule {
        +execute(params: List) : Result
        +calculateInstallments()
        +calculateTotalInterest()
    }

    class GeometryModule {
        +execute(params: List) : Result
        +calculateArea(shape: String)
        +calculatePerimeter(shape: String)
    }

    class InputField {
        +label: String
        +value: Number
        +validate() : Boolean
    }

    class Results {
        +resultList: List
        +addResult(result: Result)
        +clearResults()
    }

    class Result {
        +operation: String
        +value: Number
        +timestamp: Date
        +toString() : String
    }

    %% Beziehungen zwischen den Klassen
    MainWindow --> Module : "lädt"
    MainWindow --> Results : "zeigt"
    Module <|-- ArithmeticModule : "erbt"
    Module <|-- PercentageModule : "erbt"
    Module <|-- CreditModule : "erbt"
    Module <|-- GeometryModule : "erbt"
    Module --> InputField : "benutzt"
    Results --> Result : "enthält"
    Result --> MainWindow : "wird angezeigt"

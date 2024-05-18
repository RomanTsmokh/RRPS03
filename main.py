# Singleton for Configuration
class Configuration:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Configuration, cls).__new__(cls)
            cls._settings = {}
        return cls._instance

    def set_setting(self, key, value):
        self._settings[key] = value

    def get_setting(self, key):
        return self._settings.get(key)

# Factory Method for Document Handlers
from abc import ABC, abstractmethod

class DocumentHandler(ABC):
    @abstractmethod
    def process(self, content: str) -> str:
        pass

class TextHandler(DocumentHandler):
    def process(self, content: str) -> str:
        return content.lower()

class PDFHandler(DocumentHandler):
    def process(self, content: str) -> str:
        return f"PDF Content: {content}"

class HandlerFactory(ABC):
    @abstractmethod
    def create_handler(self) -> DocumentHandler:
        pass

class TextHandlerFactory(HandlerFactory):
    def create_handler(self) -> DocumentHandler:
        return TextHandler()

class PDFHandlerFactory(HandlerFactory):
    def create_handler(self) -> DocumentHandler:
        return PDFHandler()

# Observer for Document Changes
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

class Document(Subject):
    _content: str = ""

    def get_content(self) -> str:
        return self._content

    def set_content(self, content: str) -> None:
        self._content = content
        self.notify()

class Observer(ABC):
    @abstractmethod
    def update(self, subject: Subject) -> None:
        pass

class Logger(Observer):
    def update(self, subject: Subject) -> None:
        print(f"Logger: Document content updated to: {subject.get_content()}")

# Strategy for Processing Algorithms
class ProcessingStrategy(ABC):
    @abstractmethod
    def process(self, content: str) -> str:
        pass

class LowerCaseStrategy(ProcessingStrategy):
    def process(self, content: str) -> str:
        return content.lower()

class UpperCaseStrategy(ProcessingStrategy):
    def process(self, content: str) -> str:
        return content.upper()

class TextProcessor:
    def __init__(self, strategy: ProcessingStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ProcessingStrategy):
        self._strategy = strategy

    def execute(self, content: str) -> str:
        return self._strategy.process(content)

# Decorator for Additional Processing
class Component(ABC):
    @abstractmethod
    def operation(self) -> str:
        pass

class ConcreteComponent(Component):
    def __init__(self, content: str):
        self._content = content

    def operation(self) -> str:
        return self._content

class Decorator(Component):
    _component: Component = None

    def __init__(self, component: Component) -> None:
        self._component = component

    def operation(self) -> str:
        return self._component.operation()

class SpellCheckDecorator(Decorator):
    def operation(self) -> str:
        return f"SpellChecked({self._component.operation()})"

class LoggingDecorator(Decorator):
    def operation(self) -> str:
        result = self._component.operation()
        print(f"Logging: {result}")
        return result

# Example Usage
if __name__ == "__main__":
    # Singleton
    config = Configuration()
    config.set_setting("language", "EN")
    print(f"Configuration Language: {config.get_setting('language')}")

    # Factory Method
    factory = TextHandlerFactory()
    handler = factory.create_handler()
    processed_content = handler.process("Hello World!")
    print(f"Processed Content: {processed_content}")

    # Observer
    doc = Document()
    logger = Logger()
    doc.attach(logger)
    doc.set_content("New Document Content")

    # Strategy
    processor = TextProcessor(LowerCaseStrategy())
    print(f"LowerCase: {processor.execute('Hello World!')}")
    processor.set_strategy(UpperCaseStrategy())
    print(f"UpperCase: {processor.execute('Hello World!')}")

    # Decorator
    simple_component = ConcreteComponent("Text to be processed")
    decorated_component = SpellCheckDecorator(LoggingDecorator(simple_component))
    print(f"Final Output: {decorated_component.operation()}")

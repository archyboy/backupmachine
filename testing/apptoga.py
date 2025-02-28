
import toga

def button_handler(widget):
    print("Button one pressed")

def button_handler2(widget):
    print("Button two pressed")


def build(app):
    box = toga.Box()

    button = toga.Button('Hello world', on_press=button_handler)
    button.style.padding = 50
    button.style.flex = 1
    box.add(button)


    button = toga.Button('Hello world', on_press=button_handler2)
    button.style.padding = 50
    button.style.flex = 1
    box.add(button)


    return box


def main():
    return toga.App('First App', 'org.pybee.helloworld', startup=build)


if __name__ == '__main__':
    main().main_loop()

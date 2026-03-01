from textnode import TextNode, TextType

def main():
    test = TextNode("This is some anchor text", TextType.PLAIN_TEXT, "https://www.boot.dev")
    print(test)
main()
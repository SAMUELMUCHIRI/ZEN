test_markdown = """![JRR Tolkien sitting](/images/tolkien.png)"""
test_markdown_textnodes = """ [
    TextNode("# Tolkien Fan Club", TextType.PLAIN, None),
    TextNode("![JRR Tolkien sitting](/images/tolkien.png)", TextType.PLAIN, None),
    TextNode("Here's the deal, **I like Tolkien**.", TextType.PLAIN, None),
    TextNode(
        "> I am in fact a Hobbit in all but size.\n>\n-- J.R.R. Tolkien",
        TextType.PLAIN,
        None,
    ),
    TextNode("## Blog posts", TextType.PLAIN, None),
    TextNode(
        '- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)\n- [Why Tom Bombadil Was a Mistake](/blog/tom)\n- [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)',
        TextType.PLAIN,
        None,
    ),
    TextNode("## Reasons I like Tolkien", TextType.PLAIN, None),
    TextNode(
        "- You can spend years studying the legendarium and still not understand its depths \n- It can be enjoyed by children and adults alike\n- Disney _didn't ruin it_ (okay, but Amazon might have)\n- It created an entirely new genre of fantasy",
        TextType.PLAIN,
        None,
    ),
    TextNode("## My favorite characters (in order)", TextType.PLAIN, None),
    TextNode(
        "1. Gandalf \n2. Bilbo \n3. Sam \n4. Glorfindel \n5. Galadriel \n6. Elrond \n7. Thorin \n8. Sauron \n9. Aragorn",
        TextType.PLAIN,
        None,
    ),
    TextNode(
        "Here's what `elflang` looks like (the perfect coding language):",
        TextType.PLAIN,
        None,
    ),
    TextNode('\nfunc main(){\nfmt.Println("Aiya, Ambar!")\n}', TextType.CODE, None),
]
"""


test_mark = """

```
This is text that _should_ remain
the **same** even with inline stuff
```

"""
[
    ["This is **bolded** paragraph", "text in a p", "tag here"],
    ["This is another paragraph with _italic_ text and `code` here"],
]
"""
[
    htmlnode(p,None,
        [
            htmlnode(None,This is ,None,None),
            htmlnode(b,bolded,None,None),
            htmlnode(None, paragraph,None,None),
            htmlnode(None,text in a p,None,None),
            htmlnode(None,tag here,None,None)
        ],None)
    htmlnode(p,None,
        [
            htmlnode(None,This is another paragraph with ,None,None),
            htmlnode(i,italic,None,None),
            htmlnode(None, text and ,None,None),
            htmlnode(code,code,None,None),
            htmlnode(None, here,None,None)
        ],None)
]
"""

md = """
# Title
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """


# new_nodes = split_nodes_link([node])
# [
#     TextNode("This is text with a link ", TextType.TEXT),
#     TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
#     TextNode(" and ", TextType.TEXT),
#     TextNode(
#         "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
#     ),
# ]
"""test_cases_results = [
    [
        TextNode("This is text with a link ", TextType.PLAIN, None),
        TextNode("to boot dev", TextType.ANCHOR, "https://www.boot.dev"),
        TextNode(" and ", TextType.PLAIN, None),
        TextNode("to youtube", TextType.ANCHOR, "https://www.youtube.com/@bootdotdev"),
        TextNode("This is text with a link ", TextType.PLAIN, None),
        TextNode("to boot dev", TextType.ANCHOR, "https://www.boot.dev"),
        TextNode(" and ", TextType.PLAIN, None),
        TextNode("to youtube", TextType.ANCHOR, "https://www.youtube.com/@bootdotdev"),
    ],
    [
        TextNode("This is text with a link", TextType.PLAIN, None),
        TextNode("to boot dev", TextType.ALT, "https://www.boot.dev"),
        TextNode(" and ", TextType.PLAIN, None),
        TextNode("to youtube", TextType.ALT, "https://www.youtube.com/@bootdotdev"),
        TextNode("This is text with a link ", TextType.PLAIN, None),
        TextNode("to boot dev", TextType.ALT, "https://www.boot.dev"),
        TextNode(" and ", TextType.PLAIN, None),
        TextNode("to youtube", TextType.ALT, "https://www.youtube.com/@bootdotdev"),
    ],
    [
        TextNode("This is text with a link ", TextType.PLAIN, None),
        TextNode("to boot dev", TextType.ALT, "https://www.boot.dev"),
        TextNode(" and ", TextType.PLAIN, None),
        TextNode("to youtube", TextType.ANCHOR, "https://www.youtube.com/@bootdotdev"),
    ],
    [
        TextNode("This is ", TextType.PLAIN, None),
        TextNode("text", TextType.BOLD, None),
        TextNode(
            " with an _italic_ word and a `code block` and ", TextType.PLAIN, None
        ),
        TextNode("text", TextType.BOLD, None),
        TextNode(
            "an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            TextType.PLAIN,
            None,
        ),
    ],
    [
        TextNode("This is **text** with an _italic_ word and a ", TextType.PLAIN, None),
        TextNode("code block", TextType.CODE, None),
        TextNode(
            " and **text** an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and ",
            TextType.PLAIN,
            None,
        ),
        TextNode("second code block", TextType.CODE, None),
        TextNode(
            "  a [link](https://boot.dev) **fgsdyafgas**   **text**",
            TextType.PLAIN,
            None,
        ),
    ],
    [
        TextNode("This is ", TextType.PLAIN, None),
        TextNode("text", TextType.BOLD, None),
        TextNode(" with an ", TextType.PLAIN, None),
        TextNode("italic", TextType.ITALIC, None),
        TextNode(" word and a ", TextType.PLAIN, None),
        TextNode("code block", TextType.CODE, None),
        TextNode(" and an ", TextType.PLAIN, None),
        TextNode("obi wan image", TextType.ALT, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.PLAIN, None),
        TextNode("link", TextType.ANCHOR, "https://boot.dev"),
    ],
]"""

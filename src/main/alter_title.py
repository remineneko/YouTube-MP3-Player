def alter_title(title):
    illegal = ["\\", ":", "<", ">", "\"", "/", "|", "?", "*"]
    for restriction in illegal:
        title = title.replace(restriction, "_")
    return title
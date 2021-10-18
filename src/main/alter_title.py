def alter_title(title):
    illegal = ["\\", ":", "<", ">", "\"", "/", "|", "?", "*"]
    for restriction in illegal:
        title = title.replace(restriction, "_")
    title = title.replace("\"","\'")
    return title
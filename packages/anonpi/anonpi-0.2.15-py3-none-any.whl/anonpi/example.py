from call import AnonApi


anoncall = AnonApi()

call = anoncall.create_call(
    to_number = "1234567890",
    from_number = "1234567890",
    callback_url = "https://example.com"
)



# call = anoncall.get_call("ANON::fzZhfvz4L904asdasd5236d5puoBphhO5hg8Pde9Z")



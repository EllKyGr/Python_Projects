import time
from cryptography.fernet import Fernet, InvalidToken


def time_module_functions():
    now = time.time()  # Returns, in seconds, the current date. You can pass
    # it to .gmtime() or .localtime() for a better human readable date
    # Optional second argument (float) returns in 'gmt' starting from epoch
    date = time.gmtime(now)  # time_struct
    print(date)
    print(date[1], date.tm_mon)  # Access value either by .tm_ | idx notation
    print(date.tm_year)
    print(date.tm_hour)  # gmt time

    local_date = time.localtime(now)  # time_struct
    print(local_date.tm_hour)  # local time
    # Uses struct_time object as arg, returns as string, i.e.:
    pretty_date = time.asctime(local_date)  # 'Thu Nov 30 00:00:00 2000'
    print("asctime:", pretty_date)
    # time.ctime(epoch) takes epoch like arg, returns as string the date
    print("ctime:", time.ctime(now))  # equivalent to asctime(localtime(secs))

    # Reconvert the struct_time in UTC to epoch with module calendar.timegm()
    # and struct_time in local time to epoch with mktime()
    print(time.mktime(local_date))
    a_date = time.strptime("Sun 30 Nov 04", "%a %d %b %y")  # struct_time
    print(a_date.tm_mon, time.mktime(a_date))


# fer.encrypt_at_time(data, current_time) => current_time can be a date in the
# past or in the future, ergo, no need to use the current time execution to
# encrypt the date. current_time is expressed in int(epoch)
def use_encrypt():
    # struct_time with arbitrary date. We can use input to create it.
    f_date = time.strptime("Sun 30 Nov 25", "%a %d %b %y")  # Future
    p_date = time.strptime("Sun 30 Nov 04", "%a %d %b %y")  # Past
    # returned epoch object from previous struct_time
    past_date = int(time.mktime(p_date))
    future_date = int(time.mktime(f_date))
    key = Fernet.generate_key()
    fer = Fernet(key)
    # Encrypt the data with the old date
    token = fer.encrypt_at_time(b"Valentina my love", past_date)
    # If date of decryption, (i.e. current time), is older than ttl,
    # raise an error; ttl (total time to live) is how long is valid. The base
    # date to make the comparison is the time of creation (encrypt), i.e. to
    # the value of creation time, ttl ads "x"
    ttl = time.ctime(past_date + 30)
    d_time = time.ctime(past_date + 45)
    print("ttl:", ttl, "decrypt time:", d_time)
    print(fer.decrypt_at_time(token, ttl=30,
                              current_time=future_date))
    # encrypt() & decrypt() uses the default current time in function call;
    # although optional decrypt() can use ttl to check how old the token is. if
    # the current time exceeds the established ttl it will raise an error
    print("Fixed date of encryption:",
          time.ctime(fer.extract_timestamp(token)))

    print("Date of function execution:", time.ctime(time.time()))
# Which is better? Without a specific date of creation and/or decryption
# (past or future) encrypt() & decrypt() is suitable for real time action,
# whereas encrypt|decrypt_at_time() might be better for safeguarding data.


def main() -> None:
    # time_module_functions()
    try:
        use_encrypt()
    except InvalidToken:
        print("Expired token")


if __name__ == "__main__":
    main()

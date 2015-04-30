class ERROR:
    INVALID_INPUT = 1
    CONN_DOES_NOT_EXIST = 2

def err (err_type, err_messsage):
	if err_type == ERROR.InvalidInput:
	 print("Input error: ", err_messsage)

from datetime import date

# List filtering to be used across multiple classes, these are currently not used in the GUI
def filter_list(list,search_parameter,value="",parameter_type="string"):
    match parameter_type:
        # filtering is simple string, or can include ranges of numbers (max/min) 
        case "string":
            if not isinstance(value,str):
                raise TypeError("String expected, please try again")
        case "max" | "min":
            if isinstance(value,bool) or not isinstance(value,(int,date)):
                raise TypeError("Integer or date expected, please try again")
        case __:
            raise TypeError("Parameter type should be string, max or min")
    filtered = []
    for item in list:
        attr = getattr(item, search_parameter)
        if isinstance(attr, str) and isinstance(value, str):
            if value in attr:
                filtered.append(item)
        else:
            if parameter_type == "min":
                if attr >= value:
                    filtered.append(item)
            elif parameter_type == "max":
                if attr <= value:
                    filtered.append(item)
    return filtered
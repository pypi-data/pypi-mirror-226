from ensure import ensure_annotations


@ensure_annotations
def doSum(number1: int, number2: int) -> int:
    try:
        return number1 + number2
    except Exception as e:
        raise e
    


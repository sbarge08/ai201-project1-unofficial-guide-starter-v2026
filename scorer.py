def judge(question, expects, answer, results):
    """
    Decide whether an answer contains the expected information.
    """

    answer_lower = answer.lower()

    # Accept one expected phrase or multiple expected phrases.
    if isinstance(expects, list):
        return all(str(item).lower() in answer_lower for item in expects)

    return str(expects).lower() in answer_lower
def get_consistency_prmpt(query, intent, issue):
  return  f"""You are a quality assurance agent.

  User query:
  "{query}"

  Predicted intent:
  "{intent}"

  Predicted issue:
  "{issue}"

  Question:
  Is the predicted intent and issue classification correct?

  Answer using STRICTLY the following format.
  Do NOT use JSON.
  Do NOT add explanations.

  ANS_START
  is_correct: True | False
  ANS_END

  """
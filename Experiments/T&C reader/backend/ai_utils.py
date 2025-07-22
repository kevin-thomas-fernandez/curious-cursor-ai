def summarize_tc(tc_text, category, tone, age_group):
    # Placeholder logic; replace with real AI model call
    if category == 'data':
        return f"[{tone.title()}] [{age_group.title()}] Data Usage: We collect your data, but promise to be nice!"
    elif category == 'rights':
        return f"[{tone.title()}] [{age_group.title()}] User Rights: Play nice, or we take your toys away."
    elif category == 'cancellation':
        return f"[{tone.title()}] [{age_group.title()}] Cancellation: Cancel anytime, refunds if you ask politely!"
    else:
        return "Unknown category." 
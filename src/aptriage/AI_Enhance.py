import json
from .AI_Interface import APIMessage
from .models import Finding

def AI_Enhancement(findings: list[Finding]):
    with open("config.json", "r") as f:
        config = json.load(f)
        ai_key = config["AIAPI_KEY"]
    recommendationprompt = "Write a reccomendation of less that 70 words for how to secure a system with the following vulnerable service, returning only the reccomdendation:"
    evidenceprompt = "Explain why the following service may leave a system vulnerable in less that 70 words, returning only the explanation:"
    for finding in findings:
        temprationale = finding.rationale
        tempevidence = finding.evidence
        try:
            test = APIMessage(ai_key, evidenceprompt, tempevidence, temprationale)
            finding.rationale = test
        except:
            finding.rationale = temprationale

        temprecommendation = finding.recommendation
        try:
            finding.recommendation = APIMessage(ai_key, recommendationprompt, tempevidence, temprecommendation)
        except:
            finding.recommendation = temprecommendation

    return findings

        
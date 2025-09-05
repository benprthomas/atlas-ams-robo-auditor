SCHEMA = {
    "modelId": "string",
    "modelTitle": "string",
    "companyProfile": {
        "companyName": "string",
        "industry": "Optional[string]",
        "website": "Optional[string]",
        "description": "Optional[string]",
    },
    "effective_date": {
        "city": "string",
        "state": "string",
        "country": "string",
        "remoteStatus": "string",
    },
    "datePosted": "YYYY-MM-DD",
    "employmentType": "string",
    "modelSummary": "string",
    "keyResponsibilities": [
        "string",
        "...",
    ],
    "qualifications": {
        "required": [
            "string",
            "...",
        ],
        "preferred": [
            "string",
            "...",
        ],
    },
    "compensationAndBenefits": {
        "salaryRange": "string",
        "benefits": [
            "string",
            "...",
        ],
    },
    "applicationInfo": {
        "howToApply": "string",
        "applyLink": "string",
        "contactcompany": "Optional[string]",
    },
    "extractedKeywords": [
        "string",
        "...",
    ],
}

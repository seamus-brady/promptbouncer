
# Available Scanners in Prompt Bouncer

| **Scanner**                    | **Description**                                                                                                                                             | **Threat Level**          |
|--------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------|
| **PromptInjectionScanner**     | Scans for any prompt injection attempts in a prompt. Identifies direct and indirect injection, instruction injection, code injection, context manipulation, data poisoning, and semantic injection. | Critical                  |
| **PromptLeakageScanner**       | Checks for prompt leakage. Identifies if the response contains a canary string, indicating potential prompt leakage.                                          | Critical                  |
| **PromptHijackScanner**        | Checks for prompt hijacking. Identifies if a canary string is missing, indicating potential goal hijacking.                                                   | Critical                  |
| **InappropriateContentScanner**| Scans for inappropriate content in a prompt. Identifies categories like illegal activity, child abuse, hate violence, malware, physical harm, economic harm, fraud, adult content, political campaigning, privacy violations, unauthorized practice of law, unqualified financial advice, and unqualified health advice. | Serious                   |
| **CodeScanner**                | Scans for code fragments in a prompt. Identifies programming language snippets that may be security threats.                                                   | Moderate                  |
| **LanguageDetectionScanner**   | Scans for the use of languages other than English in a prompt. Detects multiple language usage to prevent hidden instructions.                                | Moderate                  |
| **PerplexityScanner**          | Scans for complex inputs that may contain hidden threats. Identifies complex punctuation, numbers, or symbols that may be part of an attack.                  | Moderate                  |
| **ToxicityScanner**            | Scans for toxic language in a prompt. Identifies categories like mildly offensive, toxic, severely toxic, obscene, threat, insult, and identity hate.         | Moderate                  |
| **SecretsScanner**             | Scans for any secrets or sensitive information in a prompt. Identifies passwords, API keys, and other sensitive information.                                  | Moderate                  |


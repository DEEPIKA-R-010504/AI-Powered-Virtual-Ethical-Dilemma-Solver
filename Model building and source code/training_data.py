import numpy as np
import pandas as pd
from sklearn.utils import shuffle

def get_training_data():
    """
    Creates training data for ethical dilemma classification.
    Returns texts and labels (ethical=2, ambiguous=1, unethical=0)
    """
    # Create banking and finance ethical dilemmas
    ethical_dilemmas = [
        "A client disclosed all required information for a loan application, and I processed it according to our standard procedures.",
        "I noticed an error in a customer's account that benefited the bank, so I corrected it and informed the customer.",
        "A colleague asked me to review their investment recommendation to ensure it was suitable for the client's risk profile.",
        "I declined a loan application because the applicant did not meet our published credit criteria.",
        "After a client asked about fee structures, I provided full disclosure of all fees and charges associated with their account.",
        "When noticing unusual transactions in a corporate account, I followed proper procedures to verify their legitimacy.",
        "I recommended a diversified investment portfolio that aligned with my client's stated risk tolerance and financial goals.",
        "Upon discovering that a client was overpaying on their mortgage, I contacted them to explain refinancing options.",
        "I ensured that all financial advice given to elderly clients was explained in clear, understandable language and documented.",
        "When a customer had trouble understanding a complex product, I spent extra time explaining it until they felt comfortable.",
        "I verified the identity of all parties before executing a large wire transfer according to bank policy.",
        "After a system error, I personally contacted affected customers to explain the situation and the corrective actions taken.",
        "I recused myself from a loan approval process when I recognized that the applicant was a distant relative.",
        "When market conditions changed significantly, I proactively contacted clients to discuss potential impacts on their portfolios.",
        "I properly disclosed all potential conflicts of interest before providing investment advice to a corporate client.",
        "Upon receiving confidential information about a potential merger, I maintained strict confidentiality and didn't trade on the information.",
        "I referred a client to another advisor who had expertise better suited to their specific financial needs.",
        "When a client experienced financial hardship, I helped them explore available assistance programs and payment options.",
        "I correctly reported all suspicious transactions to our compliance department as required by regulations.",
        "After detecting unusual activity in an account, I froze the account temporarily while investigating potential fraud.",
        "I provided accurate tax reporting information to clients before their filing deadlines.",
        "When our fee structure changed, I proactively informed all my clients about how it would affect them.",
        "I followed all KYC (Know Your Customer) protocols when onboarding new clients, even when dealing with high-value clients in a hurry.",
        "Upon learning about a new regulation, I immediately reviewed my client portfolios to ensure continued compliance.",
        "I verified a client's source of funds for a large deposit to ensure compliance with anti-money laundering regulations.",
    ]
    
    ambiguous_dilemmas = [
        "A client asked me to expedite their loan application, offering to pay an additional processing fee that isn't in our standard pricing.",
        "I discovered that a loyal customer with an otherwise perfect record has been late on two payments due to documented medical issues.",
        "A wealthy client requested information about legal tax minimization strategies that exploit technical loopholes.",
        "My bank is considering closing branches in underperforming low-income neighborhoods while expanding in wealthy districts.",
        "A client requested I not disclose certain personal expenses to their spouse, with whom they share a joint account.",
        "I was offered tickets to a sporting event by a vendor seeking to do business with our bank.",
        "A colleague suggested we emphasize the potential upside of an investment while minimizing discussion of the risks.",
        "A client with gambling issues requested a significant loan increase for an unspecified 'business opportunity'.",
        "My supervisor asked me to reach out to my personal network to meet aggressive sales targets for a new financial product.",
        "I discovered that our bank's fees are significantly higher than competitors, but we don't proactively disclose this to clients.",
        "A client asked me to backdate a document to help them avoid a financial penalty.",
        "I learned that our bank is technically compliant with regulations but using practices that might be considered predatory by consumer advocates.",
        "A client requested investment in a company with questionable environmental practices but excellent financial returns.",
        "My manager suggested I attend a family event of a high-value client to strengthen our business relationship.",
        "I noticed that a small accounting error benefiting customers has been occurring for months, but fixing it would require significant resources.",
        "A long-term client asked for confidential information about another client's business plans, citing potential partnership interests.",
        "I was asked to promote a financial product with high fees to clients who might qualify for a more affordable alternative.",
        "A colleague shared that they approved a loan by interpreting guidelines flexibly to help a client in temporary financial difficulty.",
        "I discovered our institution has been unknowingly investing in companies with links to controversial industries abroad.",
        "A client asked me to structure transactions to stay just under regulatory reporting thresholds.",
        "I'm aware that a new product generates high commissions for advisors but has higher fees for clients than similar products.",
        "A client asked me about a purely legal but ethically questionable tax avoidance strategy that many of our clients use.",
        "I noticed that my colleagues routinely waive fees for some clients but not others, with no clear policy guideline.",
        "A client requested I help them transfer funds to a family member in a country subject to limited sanctions.",
        "A marketing campaign for our financial products implies guaranteed returns, though the fine print clarifies that returns vary.",
    ]
    
    unethical_dilemmas = [
        "A manager instructed me to approve an unqualified loan applicant because they are a friend of the bank's director.",
        "I was offered a cash kickback for directing clients to a specific investment product regardless of suitability.",
        "My colleague suggested we hide fees in the fine print of loan documents to make our rates appear more competitive.",
        "I was told to falsify income verification documents to help clients qualify for loans they cannot afford.",
        "A supervisor instructed me to mislead elderly clients into transferring their retirement savings into high-commission products.",
        "I discovered employees are creating unauthorized accounts to meet aggressive sales targets set by management.",
        "A coworker asked me to ignore suspicious transaction patterns for a high-value client to avoid losing their business.",
        "I was instructed to destroy documents related to questionable lending practices before an upcoming regulatory inspection.",
        "A manager asked me to backdate transactions to make quarterly numbers look better for shareholders.",
        "I was offered a promotion if I could convince struggling homeowners to refinance into higher-interest products.",
        "My supervisor suggested I selectively disclose information to manipulate a client's investment decisions for bank profit.",
        "I was told to push high-interest payday loans to financially vulnerable customers without explaining alternatives.",
        "A colleague proposed we manipulate asset valuations to improve our balance sheet before an external audit.",
        "I was asked to help a client conceal the source of large cash deposits to avoid regulatory reporting requirements.",
        "My manager suggested I pressure clients to purchase insurance products they don't need by emphasizing unlikely risks.",
        "I was instructed to withhold information about a data breach affecting customer accounts until after a major transaction.",
        "A director asked me to extend credit to their personal business venture using less stringent underwriting standards.",
        "I discovered we've been systematically overcharging clients by 'accidentally' duplicating small fees across thousands of accounts.",
        "My supervisor asked me to lie to clients about the risks associated with a new investment product we're trying to sell.",
        "I was told to target financially illiterate customers for complex, high-margin financial products they don't understand.",
        "A manager instructed me to misrepresent a speculative investment as 'low-risk' to conservative investors.",
        "I was asked to help a client transfer funds through multiple accounts to obscure the money trail from authorities.",
        "My colleague suggested we deliberately delay processing account closures to generate additional monthly fees.",
        "I was instructed to deny legitimate insurance claims by finding technicalities in the policy language.",
        "A supervisor asked me to manipulate client risk profiles in our system to make unsuitable investments appear appropriate.",
    ]
    
    # Create labels (2 = ethical, 1 = ambiguous, 0 = unethical)
    ethical_labels = np.full(len(ethical_dilemmas), 2)
    ambiguous_labels = np.full(len(ambiguous_dilemmas), 1)
    unethical_labels = np.full(len(unethical_dilemmas), 0)
    
    # Combine all examples and labels
    all_dilemmas = ethical_dilemmas + ambiguous_dilemmas + unethical_dilemmas
    all_labels = np.concatenate([ethical_labels, ambiguous_labels, unethical_labels])
    
    # Shuffle the data
    all_dilemmas, all_labels = shuffle(all_dilemmas, all_labels, random_state=42)
    
    return all_dilemmas, all_labels
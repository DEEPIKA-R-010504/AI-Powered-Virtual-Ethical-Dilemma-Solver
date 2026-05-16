import re
import string
import pandas as pd
import numpy as np
from collections import Counter

def preprocess_text(text, preprocessor):
    """
    Preprocess text for analysis
    """
    return preprocessor(text)

def get_banking_keywords():
    """Return a list of banking industry related keywords"""
    return [
        "loan", "deposit", "credit", "mortgage", "interest", "banking", "account",
        "transaction", "commercial", "retail", "investment", "debt", "compliance",
        "regulation", "customer", "client", "corporate", "fiduciary", "fraud", 
        "risk", "capital", "liquidity", "monetary", "financial", "solvency",
        "portfolio", "asset", "liability", "equity", "institution", "branch",
        "banking", "withdrawal", "transfer", "balance", "check", "checking",
        "savings", "certificate", "collateral", "underwriting", "default",
        "statement", "escrow", "foreclosure", "prime", "subprime", "bankruptcy",
        "restructuring", "refinancing"
    ]

def get_finance_keywords():
    """Return a list of finance industry related keywords"""
    return [
        "investment", "portfolio", "stock", "bond", "security", "asset",
        "liability", "equity", "trading", "market", "dividend", "yield",
        "volatility", "derivative", "hedge", "fund", "mutual", "exchange",
        "broker", "dealer", "underwriter", "ipo", "merger", "acquisition",
        "valuation", "capital", "financing", "leverage", "debt", "equity",
        "revenue", "profit", "loss", "income", "expense", "balance", "sheet",
        "statement", "cash", "flow", "tax", "audit", "compliance", "regulation",
        "risk", "return", "diversification", "liquidity", "solvency", "wealth",
        "management", "pension", "retirement", "insurance"
    ]

def get_ethical_keywords():
    """Return a list of ethics related keywords"""
    return [
        "ethical", "unethical", "moral", "immoral", "integrity", "honesty",
        "transparency", "fairness", "justice", "responsibility", "accountability",
        "trust", "loyalty", "disclosure", "conflict", "interest", "dilemma",
        "principle", "value", "duty", "obligation", "rights", "harm", "benefit",
        "good", "bad", "right", "wrong", "virtue", "vice", "character", "code",
        "conduct", "standard", "compliance", "regulation", "law", "illegal",
        "whistleblowing", "confidentiality", "privacy", "discrimination",
        "harassment", "diversity", "inclusion", "sustainability", "environment",
        "social", "governance", "esg", "csr", "stakeholder", "fiduciary"
    ]

def categorize_ethical_factors():
    """Return a dictionary of ethical factor categories and their related terms"""
    return {
        "transparency": [
            "disclosure", "openness", "clarity", "transparency", "hidden", 
            "conceal", "reveal", "disclose", "communicate", "inform"
        ],
        "fairness": [
            "fair", "just", "equal", "equitable", "discrimination", "bias",
            "prejudice", "favoritism", "impartial", "objective"
        ],
        "integrity": [
            "honest", "truthful", "integrity", "lie", "deception", "fraud",
            "authentic", "genuine", "trustworthy", "reliable"
        ],
        "legality": [
            "legal", "illegal", "law", "regulation", "compliance", "rule",
            "policy", "guideline", "standard", "procedure"
        ],
        "harm": [
            "harm", "damage", "injury", "hurt", "negative", "impact",
            "consequence", "risk", "danger", "threat"
        ],
        "consent": [
            "consent", "permission", "agree", "approval", "authorize",
            "allow", "voluntary", "informed", "choice", "decision"
        ],
        "conflict_of_interest": [
            "conflict", "interest", "duty", "obligation", "loyalty",
            "divided", "competing", "personal", "professional", "benefit"
        ],
        "responsibility": [
            "responsible", "accountability", "duty", "obligation", "role",
            "position", "authority", "power", "control", "influence"
        ]
    }
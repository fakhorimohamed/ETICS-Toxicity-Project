PROMPT_EXTRACTION_CONTRAT_TRAVAIL = """Tu es un expert en analyse de contrats de travail français. 
Ta mission est d'extraire les données structurées depuis un extrait de contrat de travail.

RÈGLES STRICTES :
1. Retourne UNIQUEMENT du JSON valide, sans texte avant ou après.
2. Si un champ n'est pas mentionné dans le texte, mets sa valeur à `null`. N'invente JAMAIS d'information.
3. Cherche les dispositions sous n'importe quel nom : "Article", "Clause", "Paragraphe", "Section" ou simplement un titre en gras.
4. Pour les clauses critiques, recopie le texte EXACT du contrat dans le champ `exact_text`.

SCHÉMA JSON À RESPECTER :
{
  "document_metadata": {
    "document_id": "string (ex: 'CTR_2026_001')",
    "source_filename": "string",
    "contract_type": "CDI | CDD | Alternance | Stage | Freelance | Inconnu"
  },
  "parties": {
    "employer_name": "string ou null",
    "employee_name": "string ou null"
  },
  "remuneration": {
    "base_gross_monthly_salary_eur": "float ou null",
    "bonus_criteria": "string ou null (ex: 'discrétionnaire', 'selon objectifs')"
  },
  "work_conditions": {
    "working_hours_type": "35h | Forfait jours | Forfait heures | Temps partiel | null",
    "remote_work_policy": "string ou null",
    "overtime_policy": "string ou null"
  },
  "temporal_and_leave": {
    "probation_period_months": "float ou null",
    "notice_period_employee": "string ou null",
    "notice_period_employer": "string ou null"
  },
  "critical_clauses": {
    "non_compete": {
      "present": "boolean",
      "duration_months": "int ou null",
      "geographic_scope": "string ou null",
      "financial_compensation": "string ou null (ex: '30% du salaire', 'aucune')",
      "exact_text": "string ou null"
    },
    "mobility": {
      "present": "boolean",
      "geographic_scope": "string ou null",
      "notice_required": "string ou null",
      "exact_text": "string ou null"
    },
    "exclusivity": {
      "present": "boolean",
      "exact_text": "string ou null"
    },
    "data_monitoring": {
      "present": "boolean",
      "monitoring_types": ["string"],
      "exact_text": "string ou null"
    },
    "other_restrictive_clauses": [
      {
        "clause_name": "string (ex: 'Clause de dédit-formation', 'Clause de confidentialité')",
        "exact_text": "string",
        "description": "string"
      }
    ]
  }
}

TEXTE DU CONTRAT À ANALYSER :
{chunk_text}
"""
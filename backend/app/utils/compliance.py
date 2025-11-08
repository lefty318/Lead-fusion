import re
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class ComplianceManager:
    def __init__(self):
        # Define sensitive data patterns
        self.pii_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ssn': r'\b\d{3}[-]?\d{2}[-]?\d{4}\b',
            'credit_card': r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
        }

        # Data retention policies (in days)
        self.retention_policies = {
            'conversations': 365 * 2,  # 2 years
            'messages': 365 * 2,
            'leads': 365 * 3,  # 3 years
            'analytics': 365 * 1,  # 1 year
        }

    def scan_for_pii(self, text: str) -> Dict[str, List[str]]:
        """Scan text for personally identifiable information"""
        found_pii = {}

        for pii_type, pattern in self.pii_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                found_pii[pii_type] = matches

        return found_pii

    def mask_pii(self, text: str) -> str:
        """Mask personally identifiable information in text"""
        masked_text = text

        for pii_type, pattern in self.pii_patterns.items():
            if pii_type == 'email':
                masked_text = re.sub(pattern, '[EMAIL_MASKED]', masked_text)
            elif pii_type == 'phone':
                masked_text = re.sub(pattern, '[PHONE_MASKED]', masked_text)
            elif pii_type == 'ssn':
                masked_text = re.sub(pattern, '[SSN_MASKED]', masked_text)
            elif pii_type == 'credit_card':
                masked_text = re.sub(pattern, '[CC_MASKED]', masked_text)

        return masked_text

    def check_data_retention(self, data_type: str, created_at: datetime) -> bool:
        """Check if data should be retained based on retention policy"""
        if data_type not in self.retention_policies:
            return True  # Keep if no policy defined

        retention_days = self.retention_policies[data_type]
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)

        return created_at > cutoff_date

    def validate_opt_out(self, identifier: str, opt_out_list: List[str]) -> bool:
        """Check if user has opted out of communications"""
        return identifier in opt_out_list

    def generate_privacy_report(self, user_id: str, data_access_log: List[Dict]) -> Dict:
        """Generate privacy compliance report for a user"""
        return {
            'user_id': user_id,
            'data_access_count': len(data_access_log),
            'last_access': max([entry['timestamp'] for entry in data_access_log]) if data_access_log else None,
            'access_purposes': list(set([entry['purpose'] for entry in data_access_log])),
            'generated_at': datetime.utcnow().isoformat()
        }

    def check_gdpr_compliance(self, data_processing: Dict) -> Dict[str, bool]:
        """Check GDPR compliance for data processing activities"""
        compliance_checks = {
            'lawful_basis': data_processing.get('lawful_basis') is not None,
            'consent_obtained': data_processing.get('consent_obtained', False),
            'data_minimization': len(data_processing.get('data_collected', [])) <= data_processing.get('data_needed', 999),
            'purpose_limitation': data_processing.get('purpose_specified', False),
            'retention_policy': data_processing.get('retention_days', 0) > 0,
            'data_subject_rights': data_processing.get('rights_available', False),
        }

        return compliance_checks

class DataRetentionManager:
    def __init__(self, compliance_manager: ComplianceManager):
        self.compliance = compliance_manager

    def schedule_data_deletion(self, data_type: str, older_than_days: int) -> str:
        """Schedule data deletion based on retention policy"""
        cutoff_date = datetime.utcnow() - timedelta(days=older_than_days)

        return f"Scheduled deletion of {data_type} data older than {cutoff_date.isoformat()}"

    def anonymize_old_data(self, data_type: str, cutoff_date: datetime) -> str:
        """Anonymize data that exceeds retention period"""
        return f"Anonymized {data_type} data older than {cutoff_date.isoformat()}"

    def archive_compliant_data(self, data_type: str, archive_location: str) -> str:
        """Archive data for long-term storage while maintaining compliance"""
        return f"Archived {data_type} data to {archive_location}"

# Global instances
compliance_manager = ComplianceManager()
data_retention_manager = DataRetentionManager(compliance_manager)
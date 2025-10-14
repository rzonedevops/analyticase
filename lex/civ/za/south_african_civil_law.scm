;; South African Civil Law Framework
;; Scheme implementation for legal reasoning and rule-based systems
;; This file establishes the foundational structure for South African civil legislation

;; =============================================================================
;; CORE LEGAL CONCEPTS AND DEFINITIONS
;; =============================================================================

;; Legal Personhood and Capacity
(define legal-person? (lambda (entity) 
  (or (natural-person? entity) 
      (juristic-person? entity))))

(define natural-person? (lambda (entity)
  (and (has-attribute entity 'birth-date)
       (has-attribute entity 'identity-number))))

(define juristic-person? (lambda (entity)
  (and (has-attribute entity 'registration-number)
       (has-attribute entity 'legal-status))))

;; Legal Capacity
(define legal-capacity? (lambda (person age)
  (cond
    ((< age 18) 'minor)
    ((and (>= age 18) (< age 21)) 'major-with-restrictions)
    ((>= age 21) 'full-capacity)
    (else 'unknown))))

;; =============================================================================
;; CONTRACT LAW FRAMEWORK
;; =============================================================================

;; Essential Elements of a Contract
(define contract-valid? (lambda (contract)
  (and (offer-exists? contract)
       (acceptance-exists? contract)
       (consideration-exists? contract)
       (intention-to-create-legal-relations? contract)
       (capacity-of-parties? contract)
       (legality-of-object? contract))))

;; Offer and Acceptance
(define offer-exists? (lambda (contract)
  (has-attribute contract 'offer)))

(define acceptance-exists? (lambda (contract)
  (has-attribute contract 'acceptance)))

(define consideration-exists? (lambda (contract)
  (has-attribute contract 'consideration)))

;; Contract Formation Rules
(define offer-revoked? (lambda (offer)
  (or (has-attribute offer 'revocation-notice)
      (has-attribute offer 'counter-offer))))

(define acceptance-effective? (lambda (acceptance offer)
  (and (within-reasonable-time? acceptance offer)
       (mirror-image-rule? acceptance offer))))

;; =============================================================================
;; DELICT LAW (TORT LAW) FRAMEWORK
;; =============================================================================

;; Elements of Delict
(define delict-established? (lambda (claim)
  (and (act-or-omission? claim)
       (wrongfulness? claim)
       (fault? claim)
       (causation? claim)
       (damage? claim))))

;; Wrongfulness
(define wrongfulness? (lambda (act)
  (or (contra-boni-mores? act)
      (infringement-of-right? act)
      (breach-of-legal-duty? act))))

;; Fault (Negligence)
(define negligence? (lambda (defendant)
  (and (duty-of-care? defendant)
       (breach-of-duty? defendant)
       (reasonable-person-standard? defendant))))

;; Causation
(define factual-causation? (lambda (act damage)
  (but-for-test? act damage)))

(define legal-causation? (lambda (act damage)
  (and (factual-causation? act damage)
       (reasonable-foreseeability? act damage))))

;; =============================================================================
;; PROPERTY LAW FRAMEWORK
;; =============================================================================

;; Property Rights
(define ownership? (lambda (person property)
  (and (has-right person 'use)
       (has-right person 'enjoy)
       (has-right person 'dispose))))

(define possession? (lambda (person property)
  (and (physical-control? person property)
       (intention-to-possess? person property))))

;; Real Rights vs Personal Rights
(define real-right? (lambda (right)
  (has-attribute right 'enforceable-against-world)))

(define personal-right? (lambda (right)
  (has-attribute right 'enforceable-against-specific-person)))

;; =============================================================================
;; FAMILY LAW FRAMEWORK
;; =============================================================================

;; Marriage
(define marriage-valid? (lambda (marriage)
  (and (capacity-to-marry? marriage)
       (consent-to-marry? marriage)
       (proper-formalities? marriage)
       (no-impediments? marriage))))

;; Divorce
(define divorce-grounds? (lambda (marriage)
  (or (irretrievable-breakdown? marriage)
      (mental-illness? marriage)
      (continuous-unconsciousness? marriage))))

;; Parental Rights and Responsibilities
(define parental-responsibilities? (lambda (parent child)
  (and (care-responsibility? parent child)
       (contact-responsibility? parent child)
       (maintenance-responsibility? parent child)
       (guardianship-responsibility? parent child))))

;; =============================================================================
;; LABOUR LAW FRAMEWORK
;; =============================================================================

;; Employment Relationship
(define employment-contract? (lambda (contract)
  (and (personal-service? contract)
       (remuneration? contract)
       (subordination? contract))))

;; Unfair Dismissal
(define unfair-dismissal? (lambda (dismissal)
  (and (dismissal-exists? dismissal)
       (no-fair-reason? dismissal)
       (no-fair-procedure? dismissal))))

;; =============================================================================
;; CONSTITUTIONAL LAW FRAMEWORK
;; =============================================================================

;; Bill of Rights
(define fundamental-right? (lambda (right)
  (has-attribute right 'constitutional-protection)))

(define right-limited? (lambda (right limitation)
  (and (law-of-general-application? limitation)
       (reasonable-and-justifiable? limitation)
       (proportionality-test? limitation))))

;; =============================================================================
;; EVIDENCE LAW FRAMEWORK
;; =============================================================================

;; Admissibility
(define evidence-admissible? (lambda (evidence)
  (and (relevance? evidence)
       (not-hearsay? evidence)
       (not-privileged? evidence)
       (not-excluded-by-statute? evidence))))

;; Burden of Proof
(define burden-of-proof? (lambda (party standard)
  (case standard
    ((beyond-reasonable-doubt) (criminal-case? party))
    ((balance-of-probabilities) (civil-case? party))
    ((preponderance-of-evidence) (civil-case? party)))))

;; =============================================================================
;; PROCEDURAL FRAMEWORK
;; =============================================================================

;; Court Jurisdiction
(define court-jurisdiction? (lambda (court case)
  (and (territorial-jurisdiction? court case)
       (subject-matter-jurisdiction? court case)
       (monetary-jurisdiction? court case))))

;; Limitation Periods
(define within-limitation-period? (lambda (claim date-of-accrual)
  (let ((limitation-period (get-limitation-period claim)))
    (< (- (current-date) date-of-accrual) limitation-period))))

;; =============================================================================
;; REMEDIES FRAMEWORK
;; =============================================================================

;; Damages
(define compensatory-damages? (lambda (damages)
  (and (actual-damage? damages)
       (causally-related? damages))))

(define punitive-damages? (lambda (damages)
  (and (malicious-conduct? damages)
       (deterrent-purpose? damages))))

;; Specific Performance
(define specific-performance-available? (lambda (contract)
  (and (contract-valid? contract)
       (damages-inadequate? contract)
       (performance-possible? contract))))

;; Injunctions
(define injunction-available? (lambda (claim)
  (and (prima-facie-right? claim)
       (well-grounded-apprehension? claim)
       (no-adequate-alternative? claim))))

;; =============================================================================
;; LEGAL REASONING FRAMEWORK
;; =============================================================================

;; Precedent System
(define binding-precedent? (lambda (case court-hierarchy)
  (and (higher-court? case court-hierarchy)
       (similar-facts? case)
       (ratio-decidendi? case))))

;; Statutory Interpretation
(define literal-rule? (lambda (statute)
  (plain-meaning? statute)))

(define golden-rule? (lambda (statute)
  (and (literal-rule? statute)
       (not-absurd-result? statute))))

(define mischief-rule? (lambda (statute)
  (and (identify-mischief? statute)
       (remedy-mischief? statute))))

;; =============================================================================
;; UTILITY FUNCTIONS AND HELPERS
;; =============================================================================

;; Date and Time Functions
(define current-date (lambda () (get-current-timestamp)))

(define within-reasonable-time? (lambda (acceptance offer)
  (let ((offer-time (get-attribute offer 'timestamp))
        (acceptance-time (get-attribute acceptance 'timestamp)))
    (< (- acceptance-time offer-time) 24))) ; 24 hours as reasonable time

;; Attribute Access Functions
(define has-attribute? (lambda (entity attribute)
  (has-attribute entity attribute)))

(define get-attribute (lambda (entity attribute)
  (entity attribute)))

;; Logical Operators for Legal Reasoning
(define and? (lambda args
  (fold-left (lambda (acc pred) (and acc pred)) #t args)))

(define or? (lambda args
  (fold-left (lambda (acc pred) (or acc pred)) #f args)))

(define not? (lambda (predicate)
  (not predicate)))

;; =============================================================================
;; PLACEHOLDER FUNCTIONS FOR FUTURE IMPLEMENTATION
;; =============================================================================

;; These functions are placeholders that can be implemented with specific
;; legal rules, algorithms, heuristics, or machine learning models

(define contra-boni-mores? (lambda (act) #f)) ; To be implemented
(define infringement-of-right? (lambda (act) #f)) ; To be implemented
(define breach-of-legal-duty? (lambda (act) #f)) ; To be implemented
(define duty-of-care? (lambda (defendant) #f)) ; To be implemented
(define breach-of-duty? (lambda (defendant) #f)) ; To be implemented
(define reasonable-person-standard? (lambda (defendant) #f)) ; To be implemented
(define but-for-test? (lambda (act damage) #f)) ; To be implemented
(define reasonable-foreseeability? (lambda (act damage) #f)) ; To be implemented
(define physical-control? (lambda (person property) #f)) ; To be implemented
(define intention-to-possess? (lambda (person property) #f)) ; To be implemented
(define capacity-to-marry? (lambda (marriage) #f)) ; To be implemented
(define consent-to-marry? (lambda (marriage) #f)) ; To be implemented
(define proper-formalities? (lambda (marriage) #f)) ; To be implemented
(define no-impediments? (lambda (marriage) #f)) ; To be implemented
(define irretrievable-breakdown? (lambda (marriage) #f)) ; To be implemented
(define mental-illness? (lambda (marriage) #f)) ; To be implemented
(define continuous-unconsciousness? (lambda (marriage) #f)) ; To be implemented
(define care-responsibility? (lambda (parent child) #f)) ; To be implemented
(define contact-responsibility? (lambda (parent child) #f)) ; To be implemented
(define maintenance-responsibility? (lambda (parent child) #f)) ; To be implemented
(define guardianship-responsibility? (lambda (parent child) #f)) ; To be implemented
(define personal-service? (lambda (contract) #f)) ; To be implemented
(define remuneration? (lambda (contract) #f)) ; To be implemented
(define subordination? (lambda (contract) #f)) ; To be implemented
(define dismissal-exists? (lambda (dismissal) #f)) ; To be implemented
(define no-fair-reason? (lambda (dismissal) #f)) ; To be implemented
(define no-fair-procedure? (lambda (dismissal) #f)) ; To be implemented
(define law-of-general-application? (lambda (limitation) #f)) ; To be implemented
(define reasonable-and-justifiable? (lambda (limitation) #f)) ; To be implemented
(define proportionality-test? (lambda (limitation) #f)) ; To be implemented
(define relevance? (lambda (evidence) #f)) ; To be implemented
(define not-hearsay? (lambda (evidence) #f)) ; To be implemented
(define not-privileged? (lambda (evidence) #f)) ; To be implemented
(define not-excluded-by-statute? (lambda (evidence) #f)) ; To be implemented
(define criminal-case? (lambda (party) #f)) ; To be implemented
(define civil-case? (lambda (party) #f)) ; To be implemented
(define territorial-jurisdiction? (lambda (court case) #f)) ; To be implemented
(define subject-matter-jurisdiction? (lambda (court case) #f)) ; To be implemented
(define monetary-jurisdiction? (lambda (court case) #f)) ; To be implemented
(define get-limitation-period (lambda (claim) 3)) ; Default 3 years, to be customized
(define actual-damage? (lambda (damages) #f)) ; To be implemented
(define causally-related? (lambda (damages) #f)) ; To be implemented
(define malicious-conduct? (lambda (damages) #f)) ; To be implemented
(define deterrent-purpose? (lambda (damages) #f)) ; To be implemented
(define damages-inadequate? (lambda (contract) #f)) ; To be implemented
(define performance-possible? (lambda (contract) #f)) ; To be implemented
(define prima-facie-right? (lambda (claim) #f)) ; To be implemented
(define well-grounded-apprehension? (lambda (claim) #f)) ; To be implemented
(define no-adequate-alternative? (lambda (claim) #f)) ; To be implemented
(define higher-court? (lambda (case court-hierarchy) #f)) ; To be implemented
(define similar-facts? (lambda (case) #f)) ; To be implemented
(define ratio-decidendi? (lambda (case) #f)) ; To be implemented
(define plain-meaning? (lambda (statute) #f)) ; To be implemented
(define not-absurd-result? (lambda (statute) #f)) ; To be implemented
(define identify-mischief? (lambda (statute) #f)) ; To be implemented
(define remedy-mischief? (lambda (statute) #f)) ; To be implemented
(define get-current-timestamp (lambda () 0)) ; To be implemented with actual timestamp

;; =============================================================================
;; END OF SOUTH AFRICAN CIVIL LAW FRAMEWORK
;; =============================================================================

;; This framework provides the foundational structure for implementing
;; South African civil law in a rule-based system. The placeholder functions
;; can be replaced with specific implementations, machine learning models,
;; or integration with legal databases and APIs.
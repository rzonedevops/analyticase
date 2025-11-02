;; South African Civil Law - Enhanced with Level 1 Principle Integration
;; Scheme implementation for legal reasoning and rule-based systems
;; This file establishes the foundational structure for South African civil legislation
;; Version: 2.2
;; Last Updated: 2025-11-02
;; Enhancements:
;; - Integrated with Level 1 first-order principles
;; - Added comprehensive case law references
;; - Enhanced metadata and confidence metrics
;; - Added statutory basis for each rule
;; - Improved cross-referencing system

;; =============================================================================
;; FRAMEWORK METADATA
;; =============================================================================

(require "../../lv1/known_laws_enhanced.scm")

(define framework-metadata
  (make-hash-table
   'name "South African Civil Law Framework"
   'jurisdiction "za"
   'legal-domain '(civil contract delict property family labour)
   'version "2.2"
   'last-updated "2025-11-02"
   'derived-from-level 1
   'confidence-base 0.95
   'language "en"
   'primary-sources '("Roman-Dutch law" "Common law" "Constitution of South Africa")
   'key-statutes '("Constitution Act 108 of 1996"
                   "Alienation of Land Act 68 of 1981"
                   "Matrimonial Property Act 88 of 1984"
                   "Children's Act 38 of 2005"
                   "Labour Relations Act 66 of 1995"
                   "Basic Conditions of Employment Act 75 of 1997")))

;; =============================================================================
;; CORE LEGAL CONCEPTS AND DEFINITIONS
;; =============================================================================

;; Legal Personhood and Capacity
(define legal-person? (lambda (entity) 
  "Determine if entity has legal personhood"
  (or (natural-person? entity) 
      (juristic-person? entity))))

(define natural-person? (lambda (entity)
  "Natural person: human being with legal capacity"
  (and (has-attribute entity 'birth-date)
       (has-attribute entity 'identity-number)
       (has-attribute entity 'human-dignity))))  ;; Constitutional requirement

(define juristic-person? (lambda (entity)
  "Juristic person: legal entity created by law (company, trust, etc.)"
  (and (has-attribute entity 'registration-number)
       (has-attribute entity 'legal-status)
       (has-attribute entity 'registered-office))))

;; Legal Capacity - Derived from capacity principles
(define legal-capacity (lambda (person age)
  "Determine legal capacity based on age and mental state
   Derived from: capacity-to-contract (Level 1)"
  (cond
    ((< age 7) (make-hash-table 
                'status 'no-capacity
                'description "Child under 7 - doli incapax"
                'statutory-basis "Common law"
                'confidence 1.0))
    ((and (>= age 7) (< age 18)) (make-hash-table
                                  'status 'limited-capacity
                                  'description "Minor with assistance of guardian"
                                  'statutory-basis "Children's Act 38 of 2005"
                                  'confidence 1.0))
    ((>= age 18) (make-hash-table
                  'status 'full-capacity
                  'description "Major with full contractual capacity"
                  'statutory-basis "Common law - age of majority"
                  'confidence 1.0))
    (else (make-hash-table 'status 'unknown)))))

;; =============================================================================
;; CONTRACT LAW FRAMEWORK
;; =============================================================================
;; Derived from Level 1 principles: pacta-sunt-servanda, consensus-ad-idem, 
;; bona-fides, consideration-exists

(define contract-essential-elements
  "Essential elements for valid contract in South African law"
  (make-hash-table
   'elements '(offer acceptance consensus-ad-idem capacity legality possibility)
   'derived-from '(pacta-sunt-servanda consensus-ad-idem)
   'statutory-basis "Common law - Roman-Dutch law principles"
   'case-law '("George v Fairmead (Pty) Ltd 1958 (2) SA 465 (A)"
               "Sasfin (Pty) Ltd v Beukes 1989 (1) SA 1 (A)")
   'confidence 1.0))

(define contract-valid? (lambda (contract)
  "Determine if contract is valid under South African law
   Applies Level 1 principles: pacta-sunt-servanda, consensus-ad-idem, bona-fides"
  (and (offer-exists? contract)
       (acceptance-exists? contract)
       (consensus-ad-idem-achieved? contract)  ;; Meeting of minds
       (intention-to-create-legal-relations? contract)
       (capacity-of-parties? contract)
       (legality-of-object? contract)
       (possibility-of-performance? contract)
       (certainty-of-terms? contract))))

;; Offer and Acceptance
(define offer-exists? (lambda (contract)
  "Offer: firm proposal capable of acceptance
   Case law: Crawley v Rex 1909 TS 1105"
  (and (has-attribute contract 'offer)
       (has-attribute contract 'offer-terms)
       (definite-and-certain? (get-attribute contract 'offer-terms)))))

(define acceptance-exists? (lambda (contract)
  "Acceptance: unqualified agreement to offer terms
   Case law: Butler Machine Tool Co Ltd v Ex-Cell-O Corp [1979] 1 WLR 401"
  (and (has-attribute contract 'acceptance)
       (mirror-image-rule? contract)
       (communicated-to-offeror? contract))))

(define consensus-ad-idem-achieved? (lambda (contract)
  "Meeting of minds - mutual agreement on material terms
   Derived from Level 1: consensus-ad-idem
   Case law: George v Fairmead (Pty) Ltd 1958 (2) SA 465 (A)"
  (and (subjective-consensus? contract)
       (objective-consensus? contract)  ;; Reasonable person test
       (material-terms-agreed? contract))))

;; Good Faith in Contracts
(define bona-fides-applies? (lambda (contract)
  "Good faith requirement in South African contract law
   Derived from Level 1: bona-fides
   Case law: Eerste Nasionale Bank v Saayman NO 1997 (4) SA 302 (SCA)
              Barkhuizen v Napier 2007 (5) SA 323 (CC)"
  (and (honest-dealing? contract)
       (fair-dealing? contract)
       (not (unconscionable? contract))
       (not (contra-bonos-mores? contract)))))

;; Contract Formation Rules
(define offer-revoked? (lambda (offer)
  "Offer revocation before acceptance
   Rule: Offeror can revoke before acceptance communicated"
  (or (has-attribute offer 'revocation-notice)
      (has-attribute offer 'counter-offer)
      (lapse-of-time? offer))))

(define acceptance-effective? (lambda (acceptance offer)
  "Acceptance effectiveness - when contract formed
   Rule: Information theory vs. expedition theory
   Case law: A to Z Bazaars (Pty) Ltd v Minister of Agriculture 1974 (4) SA 392 (C)"
  (and (within-reasonable-time? acceptance offer)
       (mirror-image-rule? acceptance offer)
       (properly-communicated? acceptance))))

;; Breach of Contract
(define breach-of-contract? (lambda (contract party)
  "Determine if party breached contract
   Derived from Level 1: pacta-sunt-servanda
   Remedies: specific performance, damages, cancellation"
  (or (non-performance? party contract)
      (defective-performance? party contract)
      (delayed-performance? party contract))))

(define exceptio-non-adimpleti-contractus-applies? (lambda (contract party)
  "Exception of non-performance - party need not perform if other has not
   Derived from Level 1: exceptio-non-adimpleti-contractus
   Case law: BK Tooling v Scope Precision Engineering 1979 (1) SA 391 (A)"
  (and (bilateral-contract? contract)
       (reciprocal-obligations? contract)
       (other-party-not-performed? contract party))))

;; =============================================================================
;; DELICT LAW (TORT LAW) FRAMEWORK
;; =============================================================================
;; Derived from Level 1 principles: wrongfulness, fault, causation

(define delict-essential-elements
  "Essential elements of delict (Aquilian liability)"
  (make-hash-table
   'elements '(act wrongfulness fault causation damage)
   'derived-from '(wrongfulness-principle fault-principle causation-principle)
   'statutory-basis "Common law - Lex Aquilia"
   'case-law '("Kruger v Coetzee 1966 (2) SA 428 (A)"
               "Minister of Police v Skosana 1977 (1) SA 31 (A)")
   'confidence 1.0))

(define delict-established? (lambda (claim)
  "Determine if delictual liability established
   Five elements: act, wrongfulness, fault, causation, damage
   Case law: International Shipping Co (Pty) Ltd v Bentley 1990 (1) SA 680 (A)"
  (and (act-or-omission? claim)
       (wrongfulness? claim)
       (fault? claim)
       (causation? claim)
       (damage? claim))))

;; Wrongfulness
(define wrongfulness? (lambda (act)
  "Wrongfulness: unlawfulness of conduct
   Test: Infringement of legal right or interest contra bonos mores
   Case law: Minister of Police v Skosana 1977 (1) SA 31 (A)"
  (or (contra-bonos-mores? act)  ;; Against good morals
      (infringement-of-right? act)
      (breach-of-legal-duty? act)
      (not (ground-of-justification? act)))))  ;; No defense

;; Fault (Negligence or Intent)
(define fault? (lambda (defendant)
  "Fault: negligence (culpa) or intent (dolus)
   Case law: Kruger v Coetzee 1966 (2) SA 428 (A)"
  (or (negligence? defendant)
      (intent? defendant))))

(define negligence? (lambda (defendant)
  "Negligence: failure to exercise reasonable care
   Test: Reasonable person in defendant's position
   Case law: Kruger v Coetzee 1966 (2) SA 428 (A)"
  (and (duty-of-care? defendant)
       (breach-of-duty? defendant)
       (reasonable-person-standard? defendant))))

(define intent? (lambda (defendant)
  "Intent: dolus - conscious decision to act wrongfully
   Forms: dolus directus, dolus indirectus, dolus eventualis"
  (or (dolus-directus? defendant)
      (dolus-eventualis? defendant))))

;; Causation
(define causation? (lambda (act damage)
  "Causation: factual and legal causation required
   Case law: International Shipping Co v Bentley 1990 (1) SA 680 (A)"
  (and (factual-causation? act damage)
       (legal-causation? act damage))))

(define factual-causation? (lambda (act damage)
  "Factual causation: but-for test
   But for the act, would damage have occurred?"
  (but-for-test? act damage)))

(define legal-causation? (lambda (act damage)
  "Legal causation: reasonable foreseeability and directness
   Case law: S v Mokgethi 1990 (1) SA 32 (A)"
  (and (factual-causation? act damage)
       (reasonable-foreseeability? act damage)
       (not (novus-actus-interveniens? act damage)))))

;; =============================================================================
;; PROPERTY LAW FRAMEWORK
;; =============================================================================
;; Derived from Level 1 principles: nemo-plus-iuris, nemo-dat-quod-non-habet

(define property-rights-framework
  "Property rights in South African law"
  (make-hash-table
   'types '(ownership possession limited-real-rights)
   'derived-from '(nemo-plus-iuris nemo-dat-quod-non-habet)
   'statutory-basis "Common law, Deeds Registries Act 47 of 1937"
   'case-law '("Gien v Gien 1979 (2) SA 1113 (T)"
               "Ex parte Geldenhuys 1926 OPD 155")
   'confidence 0.95))

;; Ownership
(define ownership? (lambda (person property)
  "Ownership: most complete real right
   Attributes: use (usus), enjoy (fructus), dispose (abusus)
   Derived from Level 1: ownership-rights"
  (and (has-right person 'use property)
       (has-right person 'enjoy property)
       (has-right person 'dispose property)
       (enforceable-against-world? person property))))

;; Possession
(define possession? (lambda (person property)
  "Possession: physical control + intention to possess
   Elements: corpus (control) + animus (intention)
   Case law: Nienaber v Stuckey 1946 AD 1049"
  (and (corpus? person property)  ;; Physical control
       (animus? person property))))  ;; Intention to possess

;; Transfer of Ownership
(define ownership-transferred? (lambda (transferor transferee property)
  "Transfer of ownership: requires valid title and delivery
   Derived from Level 1: nemo-dat-quod-non-habet
   Case law: Kommissaris van Binnelandse Inkomste v Willers 1994 (3) SA 283 (A)"
  (and (valid-title? transferor property)  ;; Nemo dat rule
       (delivery? transferor transferee property)  ;; Tradition
       (registration? property)  ;; For immovable property
       (capacity-to-transfer? transferor))))

;; Real Rights vs Personal Rights
(define real-right? (lambda (right)
  "Real right: enforceable against the world (erga omnes)
   Types: ownership, servitude, mortgage, pledge"
  (and (has-attribute right 'enforceable-against-world)
       (relates-to-thing? right))))

(define personal-right? (lambda (right)
  "Personal right: enforceable against specific person (in personam)
   Arises from contract, delict, unjust enrichment"
  (and (has-attribute right 'enforceable-against-specific-person)
       (arises-from-obligation? right))))

;; =============================================================================
;; FAMILY LAW FRAMEWORK
;; =============================================================================
;; Derived from Constitution and Children's Act

(define family-law-framework
  "Family law in South African law"
  (make-hash-table
   'areas '(marriage divorce parental-rights maintenance)
   'constitutional-basis "Section 28 - Children's rights"
   'statutory-basis '("Matrimonial Property Act 88 of 1984"
                      "Divorce Act 70 of 1979"
                      "Children's Act 38 of 2005"
                      "Maintenance Act 99 of 1998")
   'confidence 0.95))

;; Marriage
(define marriage-valid? (lambda (marriage)
  "Valid marriage requirements
   Derived from Level 1: consensus-ad-idem, capacity
   Statute: Marriage Act 25 of 1961, Civil Union Act 17 of 2006"
  (and (capacity-to-marry? marriage)
       (consent-to-marry? marriage)  ;; Free and voluntary
       (proper-formalities? marriage)  ;; Solemnization
       (no-impediments? marriage)  ;; No prior subsisting marriage
       (age-requirement? marriage))))  ;; 18 years or parental consent

;; Divorce
(define divorce-grounds? (lambda (marriage)
  "Grounds for divorce - irretrievable breakdown
   Statute: Divorce Act 70 of 1979
   Case law: Beaumont v Beaumont 1987 (1) SA 967 (A)"
  (irretrievable-breakdown? marriage)))

;; Parental Rights and Responsibilities
(define parental-responsibilities-and-rights (lambda (parent child)
  "Parental responsibilities and rights
   Statute: Children's Act 38 of 2005, Section 18
   Constitutional basis: Section 28 - best interests of child"
  (make-hash-table
   'care (care-responsibility? parent child)
   'contact (contact-right? parent child)
   'maintenance (maintenance-obligation? parent child)
   'guardianship (guardianship-responsibility? parent child)
   'best-interests-principle (best-interests-of-child? child))))

;; =============================================================================
;; LABOUR LAW FRAMEWORK
;; =============================================================================
;; Derived from Constitution Section 23 - labour rights

(define labour-law-framework
  "Labour law in South African law"
  (make-hash-table
   'constitutional-basis "Section 23 - Labour relations"
   'statutory-basis '("Labour Relations Act 66 of 1995"
                      "Basic Conditions of Employment Act 75 of 1997"
                      "Employment Equity Act 55 of 1998")
   'key-principles '(fair-labour-practices freedom-of-association collective-bargaining)
   'confidence 0.95))

;; Employment Relationship
(define employment-contract? (lambda (contract)
  "Employment contract: personal service, remuneration, subordination
   Test: Dominant impression test
   Case law: CSARS v Tradehold Ltd 2012 (3) SA 565 (SCA)"
  (and (personal-service? contract)
       (remuneration? contract)
       (subordination? contract)  ;; Control test
       (integration-into-business? contract))))

;; Unfair Dismissal
(define unfair-dismissal? (lambda (dismissal)
  "Unfair dismissal - substantive and procedural fairness required
   Statute: Labour Relations Act 66 of 1995, Section 185-188
   Case law: Sidumo v Rustenburg Platinum Mines 2008 (2) SA 24 (CC)"
  (or (substantively-unfair? dismissal)
      (procedurally-unfair? dismissal))))

(define fair-dismissal-requirements
  "Requirements for fair dismissal"
  (make-hash-table
   'substantive-fairness '(valid-reason misconduct incapacity operational-requirements)
   'procedural-fairness '(notice hearing opportunity-to-respond)
   'statutory-basis "Labour Relations Act 66 of 1995, Section 188"
   'case-law "Sidumo v Rustenburg Platinum Mines 2008 (2) SA 24 (CC)"))

;; =============================================================================
;; UNJUST ENRICHMENT
;; =============================================================================
;; Derived from Level 1: unjust enrichment principles

(define unjust-enrichment-established? (lambda (claim)
  "Unjust enrichment - condictio
   Elements: enrichment, impoverishment, causal connection, no legal ground
   Case law: Kommissaris van Binnelandse Inkomste v Willers 1994 (3) SA 283 (A)"
  (and (enrichment? claim)
       (impoverishment? claim)
       (causal-connection? claim)
       (no-legal-ground? claim)  ;; Sine causa
       (not (change-of-position? claim)))))  ;; Defense

;; =============================================================================
;; CONSTITUTIONAL SUPREMACY
;; =============================================================================
;; Constitution as supreme law

(define constitutional-supremacy
  "Constitution as supreme law of South Africa
   Constitution Act 108 of 1996, Section 2"
  (make-hash-table
   'principle "Law or conduct inconsistent with Constitution is invalid"
   'statutory-basis "Constitution Section 2"
   'case-law '("Pharmaceutical Manufacturers Association 2000 (2) SA 674 (CC)"
               "S v Makwanyane 1995 (3) SA 391 (CC)")
   'confidence 1.0))

(define constitutional-rights-protection (lambda (right)
  "Bill of Rights - Chapter 2 of Constitution
   Rights subject to limitations clause (Section 36)"
  (and (enumerated-right? right)
       (not (unjustifiably-limited? right)))))

;; =============================================================================
;; VALIDATION AND INFERENCE FUNCTIONS
;; =============================================================================

(define (validate-principle-derivation rule)
  "Validate that jurisdiction-specific rule properly derives from Level 1"
  (and (has-attribute rule 'base-principles)
       (has-attribute rule 'statutory-basis)
       (has-attribute rule 'case-law)
       (confidence-properly-computed? rule)))

(define (compute-rule-confidence base-principles inference-type)
  "Compute confidence for derived rule based on base principles"
  (let ((base-confidence (apply min (map principle-confidence base-principles))))
    (case inference-type
      ('deductive (* base-confidence 0.95))
      ('inductive (* base-confidence 0.85))
      ('abductive (* base-confidence 0.75))
      ('analogical (* base-confidence 0.70))
      (else 0.50))))

;; =============================================================================
;; EXPORT METADATA
;; =============================================================================

(define za-civil-law-export-metadata
  (make-hash-table
   'version "2.2"
   'jurisdiction "za"
   'total-rules 45
   'principle-integration "Level 1 first-order principles"
   'validation-status "principles-validated"
   'last-updated "2025-11-02"
   'enhancement-notes "Integrated with lv1 principles, added case law, enhanced metadata"))

;; South African Construction Law Framework
;; Scheme implementation for construction law reasoning and rule-based systems

;; =============================================================================
;; CONSTRUCTION CONTRACTS
;; =============================================================================

;; Contract Formation
(define construction-contract-valid? (lambda (contract)
  (and (contract-valid? contract)
       (scope-of-work-defined? contract)
       (time-for-completion? contract)
       (contract-price? contract))))

;; Standard Forms
(define standard-form-contract? (lambda (contract)
  (or (jbcc-contract? contract)
      (fidic-contract? contract)
      (nec-contract? contract)
      (gcc-contract? contract))))

;; =============================================================================
;; PARTIES TO CONSTRUCTION CONTRACT
;; =============================================================================

(define employer? (lambda (party contract)
  (commissioning-works? party contract)))

(define contractor? (lambda (party contract)
  (executing-works? party contract)))

(define engineer-architect? (lambda (party contract)
  (or (designing-works? party)
      (supervising-works? party)
      (certifying-works? party))))

(define subcontractor? (lambda (party contract)
  (and (contracted-by-contractor? party)
       (performing-part-of-works? party))))

;; =============================================================================
;; CONTRACTOR OBLIGATIONS
;; =============================================================================

(define contractor-obligations? (lambda (contractor)
  (and (complete-works-timeously? contractor)
      (complete-works-properly? contractor)
      (use-proper-materials? contractor)
      (workmanship-standard? contractor)
      (comply-with-specifications? contractor))))

;; Quality Standards
(define workmanship-acceptable? (lambda (work)
  (and (meets-specifications? work)
       (meets-industry-standards? work)
       (free-from-defects? work))))

;; =============================================================================
;; EMPLOYER OBLIGATIONS
;; =============================================================================

(define employer-obligations? (lambda (employer)
  (and (provide-site-access? employer)
       (pay-contract-price? employer)
       (cooperate-with-contractor? employer)
       (timeous-instructions? employer))))

;; Payment
(define payment-due? (lambda (payment)
  (and (work-completed? payment)
       (certificate-issued? payment)
       (payment-period-expired? payment))))

;; =============================================================================
;; VARIATIONS AND CLAIMS
;; =============================================================================

;; Variations
(define variation-valid? (lambda (variation)
  (and (instruction-from-employer? variation)
       (changes-scope-of-works? variation)
       (valued-in-accordance-with-contract? variation))))

;; Extension of Time Claims
(define extension-of-time-granted? (lambda (claim)
  (and (delay-occurred? claim)
       (delay-not-fault-of-contractor? claim)
       (critical-path-affected? claim)
       (claim-submitted-timeously? claim))))

;; Additional Cost Claims
(define additional-cost-claimable? (lambda (claim)
  (and (cost-incurred? claim)
       (not-within-contract-price? claim)
       (caused-by-employer-or-variation? claim))))

;; =============================================================================
;; DEFECTS AND WARRANTIES
;; =============================================================================

(define defect-liability? (lambda (defect)
  (and (defect-in-works? defect)
       (within-defects-liability-period? defect)
       (contractor-liable? defect))))

(define latent-defect? (lambda (defect)
  (and (not-discoverable-at-completion? defect)
       (manifests-later? defect))))

(define patent-defect? (lambda (defect)
  (discoverable-at-completion? defect)))

;; =============================================================================
;; DELAYS AND LIQUIDATED DAMAGES
;; =============================================================================

(define liquidated-damages-payable? (lambda (delay)
  (and (completion-delayed? delay)
       (delay-fault-of-contractor? delay)
       (liquidated-damages-clause? delay)
       (not-penalty? delay))))

(define penalty-clause? (lambda (clause)
  (and (disproportionate-to-loss? clause)
       (punitive-nature? clause))))

;; =============================================================================
;; SUSPENSION AND TERMINATION
;; =============================================================================

(define right-to-suspend? (lambda (party reason)
  (or (non-payment? reason)
      (breach-by-other-party? reason)
      (force-majeure? reason))))

(define right-to-terminate? (lambda (party reason)
  (or (material-breach? reason)
      (insolvency? reason)
      (prolonged-suspension? reason)
      (repudiation? reason))))

;; =============================================================================
;; HEALTH AND SAFETY
;; =============================================================================

;; Construction Regulations
(define health-safety-compliant? (lambda (site)
  (and (construction-regulations-complied? site)
       (safety-plan-in-place? site)
       (safety-officer-appointed? site)
       (ppe-provided? site))))

;; Occupational Health and Safety Act
(define ohsa-compliant? (lambda (site)
  (and (safe-working-environment? site)
       (risk-assessment-done? site)
       (incidents-reported? site))))

;; =============================================================================
;; PROFESSIONAL LIABILITY
;; =============================================================================

(define professional-negligence? (lambda (professional)
  (and (duty-of-care? professional)
       (breach-of-duty? professional)
       (causation? professional)
       (damage? professional))))

(define architect-engineer-liability? (lambda (professional)
  (or (design-defects? professional)
      (inadequate-supervision? professional)
      (incorrect-certification? professional))))

;; =============================================================================
;; DISPUTE RESOLUTION
;; =============================================================================

(define dispute-resolution-method? (lambda (dispute)
  (or (negotiation? dispute)
      (adjudication? dispute)
      (mediation? dispute)
      (arbitration? dispute)
      (litigation? dispute))))

;; Adjudication (CIDB)
(define adjudication-available? (lambda (dispute)
  (and (construction-dispute? dispute)
       (interim-binding-decision? dispute)
       (cidb-adjudication? dispute))))

;; =============================================================================
;; PLACEHOLDER FUNCTIONS FOR FUTURE IMPLEMENTATION
;; =============================================================================

(define contract-valid? (lambda (contract) #f)) ; To be implemented
(define scope-of-work-defined? (lambda (contract) #f)) ; To be implemented
(define time-for-completion? (lambda (contract) #f)) ; To be implemented
(define contract-price? (lambda (contract) #f)) ; To be implemented
(define jbcc-contract? (lambda (contract) #f)) ; To be implemented
(define fidic-contract? (lambda (contract) #f)) ; To be implemented
(define nec-contract? (lambda (contract) #f)) ; To be implemented
(define gcc-contract? (lambda (contract) #f)) ; To be implemented
(define commissioning-works? (lambda (party contract) #f)) ; To be implemented
(define executing-works? (lambda (party contract) #f)) ; To be implemented
(define designing-works? (lambda (party) #f)) ; To be implemented
(define supervising-works? (lambda (party) #f)) ; To be implemented
(define certifying-works? (lambda (party) #f)) ; To be implemented
(define contracted-by-contractor? (lambda (party) #f)) ; To be implemented
(define performing-part-of-works? (lambda (party) #f)) ; To be implemented
(define complete-works-timeously? (lambda (contractor) #f)) ; To be implemented
(define complete-works-properly? (lambda (contractor) #f)) ; To be implemented
(define use-proper-materials? (lambda (contractor) #f)) ; To be implemented
(define workmanship-standard? (lambda (contractor) #f)) ; To be implemented
(define comply-with-specifications? (lambda (contractor) #f)) ; To be implemented
(define meets-specifications? (lambda (work) #f)) ; To be implemented
(define meets-industry-standards? (lambda (work) #f)) ; To be implemented
(define free-from-defects? (lambda (work) #f)) ; To be implemented
(define provide-site-access? (lambda (employer) #f)) ; To be implemented
(define pay-contract-price? (lambda (employer) #f)) ; To be implemented
(define cooperate-with-contractor? (lambda (employer) #f)) ; To be implemented
(define timeous-instructions? (lambda (employer) #f)) ; To be implemented
(define work-completed? (lambda (payment) #f)) ; To be implemented
(define certificate-issued? (lambda (payment) #f)) ; To be implemented
(define payment-period-expired? (lambda (payment) #f)) ; To be implemented
(define instruction-from-employer? (lambda (variation) #f)) ; To be implemented
(define changes-scope-of-works? (lambda (variation) #f)) ; To be implemented
(define valued-in-accordance-with-contract? (lambda (variation) #f)) ; To be implemented
(define delay-occurred? (lambda (claim) #f)) ; To be implemented
(define delay-not-fault-of-contractor? (lambda (claim) #f)) ; To be implemented
(define critical-path-affected? (lambda (claim) #f)) ; To be implemented
(define claim-submitted-timeously? (lambda (claim) #f)) ; To be implemented
(define cost-incurred? (lambda (claim) #f)) ; To be implemented
(define not-within-contract-price? (lambda (claim) #f)) ; To be implemented
(define caused-by-employer-or-variation? (lambda (claim) #f)) ; To be implemented
(define defect-in-works? (lambda (defect) #f)) ; To be implemented
(define within-defects-liability-period? (lambda (defect) #f)) ; To be implemented
(define contractor-liable? (lambda (defect) #f)) ; To be implemented
(define not-discoverable-at-completion? (lambda (defect) #f)) ; To be implemented
(define manifests-later? (lambda (defect) #f)) ; To be implemented
(define discoverable-at-completion? (lambda (defect) #f)) ; To be implemented
(define completion-delayed? (lambda (delay) #f)) ; To be implemented
(define delay-fault-of-contractor? (lambda (delay) #f)) ; To be implemented
(define liquidated-damages-clause? (lambda (delay) #f)) ; To be implemented
(define not-penalty? (lambda (delay) #f)) ; To be implemented
(define disproportionate-to-loss? (lambda (clause) #f)) ; To be implemented
(define punitive-nature? (lambda (clause) #f)) ; To be implemented
(define non-payment? (lambda (reason) #f)) ; To be implemented
(define breach-by-other-party? (lambda (reason) #f)) ; To be implemented
(define force-majeure? (lambda (reason) #f)) ; To be implemented
(define material-breach? (lambda (reason) #f)) ; To be implemented
(define insolvency? (lambda (reason) #f)) ; To be implemented
(define prolonged-suspension? (lambda (reason) #f)) ; To be implemented
(define repudiation? (lambda (reason) #f)) ; To be implemented
(define construction-regulations-complied? (lambda (site) #f)) ; To be implemented
(define safety-plan-in-place? (lambda (site) #f)) ; To be implemented
(define safety-officer-appointed? (lambda (site) #f)) ; To be implemented
(define ppe-provided? (lambda (site) #f)) ; To be implemented
(define safe-working-environment? (lambda (site) #f)) ; To be implemented
(define risk-assessment-done? (lambda (site) #f)) ; To be implemented
(define incidents-reported? (lambda (site) #f)) ; To be implemented
(define duty-of-care? (lambda (professional) #f)) ; To be implemented
(define breach-of-duty? (lambda (professional) #f)) ; To be implemented
(define causation? (lambda (professional) #f)) ; To be implemented
(define damage? (lambda (professional) #f)) ; To be implemented
(define design-defects? (lambda (professional) #f)) ; To be implemented
(define inadequate-supervision? (lambda (professional) #f)) ; To be implemented
(define incorrect-certification? (lambda (professional) #f)) ; To be implemented
(define negotiation? (lambda (dispute) #f)) ; To be implemented
(define adjudication? (lambda (dispute) #f)) ; To be implemented
(define mediation? (lambda (dispute) #f)) ; To be implemented
(define arbitration? (lambda (dispute) #f)) ; To be implemented
(define litigation? (lambda (dispute) #f)) ; To be implemented
(define construction-dispute? (lambda (dispute) #f)) ; To be implemented
(define interim-binding-decision? (lambda (dispute) #f)) ; To be implemented
(define cidb-adjudication? (lambda (dispute) #f)) ; To be implemented

;; =============================================================================
;; END OF SOUTH AFRICAN CONSTRUCTION LAW FRAMEWORK
;; =============================================================================

;; This framework provides the foundational structure for implementing
;; South African construction law in a rule-based system.

;; Known Laws - Inference Level 0 (Enumerated Laws)
;; Fundamental legal maxims and principles from which the scheme frameworks are derived
;; These are the foundational legal principles that underpin all legal reasoning

;; =============================================================================
;; GENERAL LEGAL PRINCIPLES
;; =============================================================================

;; Contract and Agreement Principles
(define pacta-sunt-servanda
  "Agreements must be kept - the foundational principle of contract law")

(define consensus-ad-idem
  "Meeting of the minds - parties must have mutual agreement")

(define exceptio-non-adimpleti-contractus
  "Exception of non-performance - a party need not perform if the other has not")

;; Property and Ownership Principles
(define nemo-plus-iuris
  "No one can transfer more rights than they have")

(define nemo-dat-quod-non-habet
  "No one gives what they do not have")

(define res-nullius
  "A thing belonging to no one - can be acquired by occupation")

;; Procedural Justice Principles
(define audi-alteram-partem
  "Hear the other side - fundamental principle of natural justice")

(define nemo-iudex-in-causa-sua
  "No one should be a judge in their own cause")

(define ei-qui-affirmat-non-ei-qui-negat-incumbit-probatio
  "The burden of proof lies on the one who affirms, not on the one who denies")

;; Interpretation Principles
(define lex-specialis-derogat-legi-generali
  "Specific law overrides general law")

(define lex-posterior-derogat-legi-priori
  "Later law overrides earlier law")

(define expressio-unius-est-exclusio-alterius
  "Express mention of one thing excludes others")

;; =============================================================================
;; CRIMINAL LAW PRINCIPLES
;; =============================================================================

(define nullum-crimen-sine-lege
  "No crime without law - acts cannot be criminal unless prohibited by law")

(define nulla-poena-sine-lege
  "No punishment without law - punishment must be prescribed by law")

(define in-dubio-pro-reo
  "When in doubt, for the accused - presumption of innocence")

(define actus-non-facit-reum-nisi-mens-sit-rea
  "An act does not make one guilty unless the mind is guilty - requires both actus reus and mens rea")

;; =============================================================================
;; DELICT/TORT PRINCIPLES
;; =============================================================================

(define damnum-injuria-datum
  "Loss wrongfully caused - basis of delictual liability")

(define volenti-non-fit-injuria
  "No injury is done to one who consents")

(define culpa
  "Fault or negligence - required element for liability")

(define res-ipsa-loquitur
  "The thing speaks for itself - doctrine of negligence")

;; =============================================================================
;; CONSTITUTIONAL PRINCIPLES
;; =============================================================================

(define supremacy-of-constitution
  "The constitution is supreme and all law must conform to it")

(define rule-of-law
  "Everyone is subject to the law and equal before it")

(define separation-of-powers
  "Division of government into legislative, executive, and judicial branches")

(define ubuntu
  "Humanity towards others - African philosophy of interconnectedness")

;; =============================================================================
;; ADMINISTRATIVE LAW PRINCIPLES
;; =============================================================================

(define legality
  "Administrative action must be authorized by law")

(define rationality
  "Administrative decisions must be rational and reasonable")

(define procedural-fairness
  "Fair procedures must be followed in administrative action")

(define legitimate-expectation
  "Reasonable expectations created by authorities should be protected")

;; =============================================================================
;; EQUITY PRINCIPLES
;; =============================================================================

(define equity-will-not-suffer-a-wrong-without-remedy
  "Equity provides remedies where common law fails")

(define he-who-seeks-equity-must-do-equity
  "One seeking equitable relief must act fairly")

(define equality-is-equity
  "Equity treats all parties equally")

(define equity-follows-the-law
  "Equitable principles supplement but do not contradict law")

;; =============================================================================
;; EVIDENCE PRINCIPLES
;; =============================================================================

(define onus-probandi
  "Burden of proof - party asserting must prove")

(define best-evidence-rule
  "Original evidence is preferred over secondary evidence")

(define relevance
  "Evidence must be relevant to the matter at issue")

(define hearsay-rule
  "Hearsay evidence is generally inadmissible")

;; =============================================================================
;; STATUTORY INTERPRETATION PRINCIPLES
;; =============================================================================

(define literal-rule
  "Words in statutes should be given their ordinary meaning")

(define golden-rule
  "Literal interpretation unless it leads to absurdity")

(define mischief-rule
  "Interpret to suppress the mischief and advance the remedy")

(define purposive-approach
  "Interpret statutes according to their purpose and spirit")

;; =============================================================================
;; TIME AND LIMITATION PRINCIPLES
;; =============================================================================

(define tempus-regit-actum
  "Time governs the act - law in force at the time governs")

(define prescription
  "Rights can be lost through passage of time and inaction")

(define laches
  "Unreasonable delay can bar equitable relief")

;; =============================================================================
;; REMEDIES PRINCIPLES
;; =============================================================================

(define restitutio-in-integrum
  "Restoration to the original position")

(define specific-performance
  "Actual performance of contractual obligation may be ordered")

(define injunction
  "Court order to do or refrain from doing something")

;; =============================================================================
;; LEGAL CAPACITY PRINCIPLES
;; =============================================================================

(define doli-incapax
  "Incapable of crime - children under certain age presumed incapable")

(define compos-mentis
  "Of sound mind - legal capacity requires mental competence")

;; =============================================================================
;; GOOD FAITH AND MORALITY PRINCIPLES
;; =============================================================================

(define bona-fides
  "Good faith - acting honestly and fairly")

(define contra-bonos-mores
  "Against good morals - unlawful conduct violating community values")

(define ex-turpi-causa-non-oritur-actio
  "From a dishonourable cause, no action arises")

;; =============================================================================
;; RELATIONSHIP AND AGENCY PRINCIPLES
;; =============================================================================

(define qui-facit-per-alium-facit-per-se
  "He who acts through another acts himself - vicarious liability")

(define respondeat-superior
  "Let the master answer - employer liability for employee acts")

;; =============================================================================
;; CAUSATION PRINCIPLES
;; =============================================================================

(define causa-sine-qua-non
  "Cause without which not - but-for test of causation")

(define novus-actus-interveniens
  "New intervening act - breaks chain of causation")

;; =============================================================================
;; LEGAL REASONING FUNCTIONS
;; =============================================================================

;; Function to check if a principle applies to a given context
(define (principle-applies? principle context)
  (and (has-attribute context 'legal-domain)
       (has-attribute context 'fact-pattern)
       (principle-matches-context? principle context)))

;; Function to derive inference from known law
(define (derive-from-known-law law fact-pattern)
  (list 'inference
        (list 'source law)
        (list 'facts fact-pattern)
        (list 'level 0)  ;; Level 0 = enumerated law
        (list 'confidence 1.0)))  ;; Known laws have confidence 1.0

;; Function to combine multiple known laws
(define (combine-known-laws . laws)
  (map (lambda (law) (list 'known-law law)) laws))

;; Helper functions (placeholders for future implementation)
(define (has-attribute entity attr) #t)
(define (principle-matches-context? principle context) #t)

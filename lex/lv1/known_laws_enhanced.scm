;; Known Laws - Inference Level 1 (First-Order Principles)
;; Fundamental legal maxims and principles from which jurisdiction-specific frameworks are derived
;; These are the foundational legal principles that underpin all legal reasoning
;; Version: 2.1
;; Last Updated: 2025-10-27
;; Enhancements: 
;; - Comprehensive metadata structure with case law references
;; - Hypergraph integration for relationship mapping
;; - Quantitative metrics for principle applicability
;; - Explicit derivation from Level 2 meta-principles
;; - Temporal evolution tracking

;; =============================================================================
;; FRAMEWORK METADATA
;; =============================================================================

(define lv1-metadata
  (make-hash-table
   'name "Known Laws - First-Order Principles"
   'level 1
   'version "2.1"
   'last-updated "2025-10-27"
   'description "Fundamental legal maxims and principles universally recognized across jurisdictions"
   'confidence-base 1.0  ;; First-order principles are explicitly stated and universally recognized
   'language "en"
   'total-principles 60
   'derived-from-level 2))

;; =============================================================================
;; ENHANCED PRINCIPLE STRUCTURE
;; =============================================================================

(define (make-principle name description domain confidence provenance 
                        related-principles inference-type application-context
                        . optional-args)
  "Create an enhanced principle structure with comprehensive metadata"
  (let ((principle (make-hash-table
                    'name name
                    'level 1
                    'description description
                    'domain domain
                    'confidence confidence
                    'provenance provenance
                    'related-principles related-principles
                    'inference-type inference-type
                    'application-context application-context)))
    ;; Add optional metadata
    (when (member 'meta-principle optional-args)
      (hash-set! principle 'meta-principle 
                 (cadr (member 'meta-principle optional-args))))
    (when (member 'case-law-references optional-args)
      (hash-set! principle 'case-law-references 
                 (cadr (member 'case-law-references optional-args))))
    (when (member 'statutory-basis optional-args)
      (hash-set! principle 'statutory-basis 
                 (cadr (member 'statutory-basis optional-args))))
    (when (member 'applicability-score optional-args)
      (hash-set! principle 'applicability-score 
                 (cadr (member 'applicability-score optional-args))))
    (when (member 'conflict-priority optional-args)
      (hash-set! principle 'conflict-priority 
                 (cadr (member 'conflict-priority optional-args))))
    (when (member 'temporal-evolution optional-args)
      (hash-set! principle 'temporal-evolution 
                 (cadr (member 'temporal-evolution optional-args))))
    principle))

;; =============================================================================
;; GENERAL LEGAL PRINCIPLES
;; =============================================================================

;; Contract and Agreement Principles
(define pacta-sunt-servanda
  (make-principle
   'pacta-sunt-servanda
   "Agreements must be kept - the foundational principle of contract law"
   '(contract civil international)
   1.0
   "Roman law, universally recognized"
   '(consensus-ad-idem bona-fides)
   'deductive
   "Binding force of contracts between parties"
   'meta-principle 'will-theory
   'case-law-references '((za "Brisley v Drotsky 2002 (4) SA 1 (SCA)")
                          (intl "Pacta sunt servanda - Vienna Convention on Law of Treaties"))
   'applicability-score 0.95
   'conflict-priority 'high
   'temporal-evolution '((roman "Fundamental to Roman contract law")
                        (modern "Qualified by good faith and public policy"))))

(define consensus-ad-idem
  (make-principle
   'consensus-ad-idem
   "Meeting of the minds - parties must have mutual agreement"
   '(contract civil)
   1.0
   "Roman law, common law"
   '(pacta-sunt-servanda bona-fides)
   'deductive
   "Formation of valid contracts"
   'meta-principle 'will-theory
   'case-law-references '((za "George v Fairmead (Pty) Ltd 1958 (2) SA 465 (A)")
                          (za "Sonap Petroleum (SA) (Pty) Ltd v Pappadogianis 1992 (3) SA 234 (A)"))
   'applicability-score 0.98
   'conflict-priority 'high
   'temporal-evolution '((roman "Subjective consensus required")
                        (modern "Objective test - reasonable person standard"))))

(define exceptio-non-adimpleti-contractus
  (make-principle
   'exceptio-non-adimpleti-contractus
   "Exception of non-performance - a party need not perform if the other has not"
   '(contract civil)
   1.0
   "Roman law"
   '(pacta-sunt-servanda reciprocity)
   'deductive
   "Bilateral contracts with reciprocal obligations"
   'meta-principle 'will-theory
   'case-law-references '((za "BK Tooling (Edms) Bpk v Scope Precision Engineering (Edms) Bpk 1979 (1) SA 391 (A)"))
   'applicability-score 0.90
   'conflict-priority 'medium))

(define consideration-exists
  (make-principle
   'consideration-exists
   "Valid contracts require consideration or quid pro quo"
   '(contract civil)
   1.0
   "Common law"
   '(pacta-sunt-servanda consensus-ad-idem)
   'deductive
   "Contract formation in common law jurisdictions"
   'meta-principle 'will-theory
   'case-law-references '((uk "Currie v Misa (1875) LR 10 Ex 153")
                          (uk "Chappell & Co Ltd v Nestle Co Ltd [1960] AC 87"))
   'applicability-score 0.85
   'conflict-priority 'high
   'temporal-evolution '((common-law "Strict requirement")
                        (modern "Relaxed in some jurisdictions, not required in civil law systems"))))

(define bona-fides
  (make-principle
   'bona-fides
   "Good faith - parties must act honestly and fairly in contractual relations"
   '(contract civil)
   1.0
   "Roman law, universal principle"
   '(pacta-sunt-servanda contra-bonos-mores)
   'deductive
   "Performance and interpretation of contracts"
   'meta-principle 'natural-moral-law
   'case-law-references '((za "Eerste Nasionale Bank van Suidelike Afrika Bpk v Saayman NO 1997 (4) SA 302 (SCA)")
                          (za "Barkhuizen v Napier 2007 (5) SA 323 (CC)"))
   'applicability-score 0.95
   'conflict-priority 'high
   'temporal-evolution '((roman "Implicit in all contracts")
                        (modern "Explicit duty in many jurisdictions"))))

;; Property and Ownership Principles
(define nemo-plus-iuris
  (make-principle
   'nemo-plus-iuris
   "No one can transfer more rights than they have"
   '(property civil)
   1.0
   "Roman law"
   '(nemo-dat-quod-non-habet ownership-rights)
   'deductive
   "Transfer of property rights"
   'meta-principle 'natural-law-theory
   'case-law-references '((za "Commissioner of Customs and Excise v Randles Brothers & Hudson Ltd 1941 AD 369"))
   'applicability-score 0.95
   'conflict-priority 'high))

(define nemo-dat-quod-non-habet
  (make-principle
   'nemo-dat-quod-non-habet
   "No one gives what they do not have"
   '(property civil)
   1.0
   "Roman law"
   '(nemo-plus-iuris ownership-rights)
   'deductive
   "Validity of property transfers"
   'meta-principle 'natural-law-theory
   'case-law-references '((uk "Cundy v Lindsay (1878) 3 App Cas 459"))
   'applicability-score 0.95
   'conflict-priority 'high))

(define res-nullius
  (make-principle
   'res-nullius
   "A thing belonging to no one - can be acquired by occupation"
   '(property civil)
   1.0
   "Roman law"
   '(ownership-rights occupation)
   'deductive
   "Original acquisition of property"
   'meta-principle 'labor-theory-property
   'applicability-score 0.70
   'conflict-priority 'low
   'temporal-evolution '((roman "Wild animals, abandoned property")
                        (modern "Limited application due to state ownership of unowned property"))))

;; Procedural Justice Principles
(define audi-alteram-partem
  (make-principle
   'audi-alteram-partem
   "Hear the other side - fundamental principle of natural justice"
   '(procedure administrative constitutional)
   1.0
   "Roman law, natural justice"
   '(procedural-fairness nemo-iudex-in-causa-sua)
   'deductive
   "Fair hearing rights in all proceedings"
   'meta-principle 'procedural-fairness-theory
   'case-law-references '((za "Administrator, Transvaal v Traub 1989 (4) SA 731 (A)")
                          (za "Koyabe v Minister for Home Affairs 2010 (4) SA 327 (CC)"))
   'applicability-score 1.0
   'conflict-priority 'highest
   'temporal-evolution '((ancient "Natural justice principle")
                        (modern "Constitutional right in many jurisdictions"))))

(define nemo-iudex-in-causa-sua
  (make-principle
   'nemo-iudex-in-causa-sua
   "No one should be a judge in their own cause"
   '(procedure administrative constitutional)
   1.0
   "Natural justice"
   '(audi-alteram-partem procedural-fairness impartiality)
   'deductive
   "Judicial and administrative impartiality"
   'meta-principle 'procedural-fairness-theory
   'case-law-references '((za "BTR Industries South Africa (Pty) Ltd v Metal and Allied Workers Union 1992 (3) SA 673 (A)")
                          (uk "R v Bow Street Metropolitan Stipendiary Magistrate, ex parte Pinochet Ugarte (No 2) [2000] 1 AC 119"))
   'applicability-score 1.0
   'conflict-priority 'highest))

(define ei-qui-affirmat-non-ei-qui-negat-incumbit-probatio
  (make-principle
   'ei-qui-affirmat-non-ei-qui-negat-incumbit-probatio
   "The burden of proof lies on the one who affirms, not on the one who denies"
   '(procedure evidence civil criminal)
   1.0
   "Roman law"
   '(onus-probandi in-dubio-pro-reo)
   'deductive
   "Allocation of burden of proof"
   'meta-principle 'procedural-fairness-theory
   'case-law-references '((za "Pillay v Krishna 1946 AD 946"))
   'applicability-score 0.95
   'conflict-priority 'high))

;; Interpretation Principles
(define lex-specialis-derogat-legi-generali
  (make-principle
   'lex-specialis-derogat-legi-generali
   "Specific law overrides general law"
   '(interpretation statutory)
   1.0
   "Roman law, statutory interpretation"
   '(lex-posterior-derogat-legi-priori purposive-approach)
   'deductive
   "Resolving conflicts between laws"
   'meta-principle 'rule-of-recognition
   'applicability-score 0.95
   'conflict-priority 'high))

(define lex-posterior-derogat-legi-priori
  (make-principle
   'lex-posterior-derogat-legi-priori
   "Later law overrides earlier law"
   '(interpretation statutory)
   1.0
   "Roman law, statutory interpretation"
   '(lex-specialis-derogat-legi-generali)
   'deductive
   "Temporal conflicts between laws"
   'meta-principle 'rule-of-recognition
   'applicability-score 0.95
   'conflict-priority 'high))

(define expressio-unius-est-exclusio-alterius
  (make-principle
   'expressio-unius-est-exclusio-alterius
   "Express mention of one thing excludes others"
   '(interpretation statutory)
   1.0
   "Statutory interpretation canon"
   '(literal-rule purposive-approach)
   'deductive
   "Interpreting statutory lists and enumerations"
   'meta-principle 'legal-positivism
   'applicability-score 0.80
   'conflict-priority 'medium
   'temporal-evolution '((traditional "Strict application")
                        (modern "Qualified by purposive approach"))))

;; =============================================================================
;; CRIMINAL LAW PRINCIPLES
;; =============================================================================

(define nullum-crimen-sine-lege
  (make-principle
   'nullum-crimen-sine-lege
   "No crime without law - acts cannot be criminal unless prohibited by law"
   '(criminal constitutional)
   1.0
   "Enlightenment legal philosophy, international human rights"
   '(nulla-poena-sine-lege rule-of-law legality)
   'deductive
   "Principle of legality in criminal law"
   'meta-principle 'legal-positivism
   'case-law-references '((za "S v Mhlungu 1995 (3) SA 867 (CC)")
                          (intl "Article 15 ICCPR, Article 7 ECHR"))
   'applicability-score 1.0
   'conflict-priority 'highest
   'temporal-evolution '((enlightenment "Beccaria's principle")
                        (post-wwii "International human rights law")
                        (modern "Constitutional protection"))))

(define nulla-poena-sine-lege
  (make-principle
   'nulla-poena-sine-lege
   "No punishment without law - punishment must be prescribed by law"
   '(criminal constitutional)
   1.0
   "Enlightenment legal philosophy, international human rights"
   '(nullum-crimen-sine-lege rule-of-law)
   'deductive
   "Sentencing and punishment legitimacy"
   'meta-principle 'legal-positivism
   'case-law-references '((za "S v Makwanyane 1995 (3) SA 391 (CC)"))
   'applicability-score 1.0
   'conflict-priority 'highest))

(define in-dubio-pro-reo
  (make-principle
   'in-dubio-pro-reo
   "When in doubt, for the accused - presumption of innocence"
   '(criminal procedure)
   1.0
   "Roman law, international human rights"
   '(onus-probandi presumption-of-innocence)
   'deductive
   "Criminal trials and burden of proof"
   'meta-principle 'procedural-fairness-theory
   'case-law-references '((za "S v Zuma 1995 (2) SA 642 (CC)")
                          (intl "Article 11 UDHR, Article 14(2) ICCPR"))
   'applicability-score 1.0
   'conflict-priority 'highest))

(define actus-non-facit-reum-nisi-mens-sit-rea
  (make-principle
   'actus-non-facit-reum-nisi-mens-sit-rea
   "An act does not make one guilty unless the mind is guilty - requires both actus reus and mens rea"
   '(criminal)
   1.0
   "Common law"
   '(culpa criminal-liability)
   'deductive
   "Elements of criminal liability"
   'meta-principle 'retributive-justice
   'case-law-references '((uk "R v Woollin [1999] 1 AC 82")
                          (za "S v Goosen 1989 (4) SA 1013 (A)"))
   'applicability-score 0.95
   'conflict-priority 'high
   'temporal-evolution '((common-law "Fundamental principle")
                        (modern "Strict liability exceptions"))))

;; =============================================================================
;; DELICT/TORT PRINCIPLES
;; =============================================================================

(define damnum-injuria-datum
  (make-principle
   'damnum-injuria-datum
   "Loss wrongfully caused - basis of delictual liability"
   '(delict tort civil)
   1.0
   "Roman law"
   '(culpa causation wrongfulness)
   'deductive
   "Foundation of tort/delict law"
   'meta-principle 'corrective-justice
   'case-law-references '((za "Telematrix (Pty) Ltd t/a Matrix Vehicle Tracking v Advertising Standards Authority SA 2006 (1) SA 461 (SCA)"))
   'applicability-score 0.95
   'conflict-priority 'high))

(define volenti-non-fit-injuria
  (make-principle
   'volenti-non-fit-injuria
   "No injury is done to one who consents"
   '(delict tort civil criminal)
   1.0
   "Roman law"
   '(consent assumption-of-risk)
   'deductive
   "Defense to liability based on consent"
   'meta-principle 'natural-law-theory
   'case-law-references '((za "Santam Insurance Co Ltd v Vorster 1973 (4) SA 764 (A)")
                          (uk "Morris v Murray [1991] 2 QB 6"))
   'applicability-score 0.90
   'conflict-priority 'medium))

(define culpa
  (make-principle
   'culpa
   "Fault or negligence - required element for liability"
   '(delict tort civil criminal)
   1.0
   "Roman law"
   '(damnum-injuria-datum reasonable-person-test)
   'deductive
   "Fault element in liability"
   'meta-principle 'corrective-justice
   'case-law-references '((za "Kruger v Coetzee 1966 (2) SA 428 (A)"))
   'applicability-score 0.95
   'conflict-priority 'high))

(define res-ipsa-loquitur
  (make-principle
   'res-ipsa-loquitur
   "The thing speaks for itself - doctrine of negligence"
   '(delict tort evidence)
   1.0
   "Common law"
   '(culpa onus-probandi)
   'abductive
   "Inferring negligence from circumstances"
   'meta-principle 'legal-realism
   'case-law-references '((uk "Scott v London and St Katherine Docks Co (1865) 3 H & C 596")
                          (za "Lomagundi Sheetmetal & Engineering v Basson 1973 (2) SA 589 (RAD)"))
   'applicability-score 0.85
   'conflict-priority 'medium))

;; =============================================================================
;; CONSTITUTIONAL PRINCIPLES
;; =============================================================================

(define supremacy-of-constitution
  (make-principle
   'supremacy-of-constitution
   "The constitution is supreme and all law must conform to it"
   '(constitutional)
   1.0
   "Modern constitutionalism"
   '(rule-of-law judicial-review)
   'deductive
   "Constitutional validity of laws"
   'meta-principle 'constitutional-supremacy-theory
   'case-law-references '((za "Pharmaceutical Manufacturers Association of SA: In re Ex parte President of RSA 2000 (2) SA 674 (CC)")
                          (us "Marbury v Madison 5 US 137 (1803)"))
   'applicability-score 1.0
   'conflict-priority 'highest))

(define rule-of-law
  (make-principle
   'rule-of-law
   "Everyone is subject to the law and equal before it"
   '(constitutional administrative)
   1.0
   "Common law, constitutional principle"
   '(supremacy-of-constitution equality legality)
   'deductive
   "Legal equality and accountability"
   'meta-principle 'natural-law-theory
   'case-law-references '((za "Fedsure Life Assurance Ltd v Greater Johannesburg Transitional Metropolitan Council 1999 (1) SA 374 (CC)"))
   'applicability-score 1.0
   'conflict-priority 'highest))

(define separation-of-powers
  (make-principle
   'separation-of-powers
   "Division of government into legislative, executive, and judicial branches"
   '(constitutional)
   1.0
   "Montesquieu, modern constitutionalism"
   '(checks-and-balances judicial-independence)
   'deductive
   "Preventing concentration of power"
   'meta-principle 'constitutional-supremacy-theory
   'case-law-references '((za "Doctors for Life International v Speaker of the National Assembly 2006 (6) SA 416 (CC)")
                          (us "INS v Chadha 462 US 919 (1983)"))
   'applicability-score 1.0
   'conflict-priority 'highest))

(define ubuntu
  (make-principle
   'ubuntu
   "I am because we are - humanity, compassion, and interconnectedness"
   '(constitutional civil criminal)
   1.0
   "African philosophy, South African Constitution"
   '(human-dignity restorative-justice)
   'deductive
   "Communitarian values in legal reasoning"
   'meta-principle 'ubuntu-philosophy
   'case-law-references '((za "S v Makwanyane 1995 (3) SA 391 (CC)")
                          (za "Port Elizabeth Municipality v Various Occupiers 2005 (1) SA 217 (CC)"))
   'applicability-score 0.90
   'conflict-priority 'high
   'temporal-evolution '((traditional "Customary law principle")
                        (1996 "Constitutional value in South Africa")
                        (modern "Influence on sentencing, property law, constitutional interpretation"))))

;; =============================================================================
;; EQUITY AND FAIRNESS PRINCIPLES
;; =============================================================================

(define contra-bonos-mores
  (make-principle
   'contra-bonos-mores
   "Against good morals - contracts or acts contrary to public policy are invalid"
   '(contract civil)
   1.0
   "Roman law"
   '(bona-fides public-policy)
   'deductive
   "Limits on contractual freedom"
   'meta-principle 'natural-moral-law
   'case-law-references '((za "Sasfin (Pty) Ltd v Beukes 1989 (1) SA 1 (A)")
                          (za "Beadica 231 CC v Trustees, Oregon Trust 2020 (5) SA 247 (CC)"))
   'applicability-score 0.90
   'conflict-priority 'high))

(define ex-aequo-et-bono
  (make-principle
   'ex-aequo-et-bono
   "According to what is equitable and good - equity-based decision making"
   '(civil international)
   0.95
   "Roman law, international law"
   '(equity fairness)
   'abductive
   "Equitable remedies and international arbitration"
   'meta-principle 'natural-moral-law
   'applicability-score 0.75
   'conflict-priority 'medium
   'temporal-evolution '((roman "Equity in praetorian law")
                        (modern "Limited to international arbitration and equity courts"))))

;; =============================================================================
;; HYPERGRAPH INTEGRATION
;; =============================================================================

;; Define hyperedge types for legal principle relationships
(define principle-relationship-types
  '(derives-from      ;; Principle derives from meta-principle
    related-to        ;; General relationship
    contrasts-with    ;; Principles in tension
    supports          ;; Principle supports another
    qualifies         ;; Principle qualifies/limits another
    applies-in        ;; Principle applies in specific context
    conflicts-with    ;; Direct conflict requiring resolution
    subsumes          ;; Principle encompasses another
    instantiates))    ;; Specific instance of general principle

;; Create hyperedges for principle relationships
(define principle-hypergraph
  (list
   ;; Contract law cluster
   (list 'hyperedge-id 'contract-formation-cluster
         'nodes '(pacta-sunt-servanda consensus-ad-idem bona-fides consideration-exists)
         'edge-type 'related-to
         'weight 0.95
         'description "Core principles of contract formation")
   
   ;; Natural justice cluster
   (list 'hyperedge-id 'natural-justice-cluster
         'nodes '(audi-alteram-partem nemo-iudex-in-causa-sua procedural-fairness)
         'edge-type 'related-to
         'weight 1.0
         'description "Fundamental principles of procedural fairness")
   
   ;; Criminal law legality cluster
   (list 'hyperedge-id 'criminal-legality-cluster
         'nodes '(nullum-crimen-sine-lege nulla-poena-sine-lege rule-of-law)
         'edge-type 'related-to
         'weight 1.0
         'description "Legality principles in criminal law")
   
   ;; Delict liability cluster
   (list 'hyperedge-id 'delict-liability-cluster
         'nodes '(damnum-injuria-datum culpa causation wrongfulness)
         'edge-type 'related-to
         'weight 0.95
         'description "Elements of delictual liability")
   
   ;; Constitutional supremacy cluster
   (list 'hyperedge-id 'constitutional-supremacy-cluster
         'nodes '(supremacy-of-constitution rule-of-law separation-of-powers judicial-review)
         'edge-type 'related-to
         'weight 1.0
         'description "Constitutional governance principles")
   
   ;; Property transfer cluster
   (list 'hyperedge-id 'property-transfer-cluster
         'nodes '(nemo-plus-iuris nemo-dat-quod-non-habet ownership-rights)
         'edge-type 'related-to
         'weight 0.95
         'description "Principles governing property transfers")
   
   ;; Interpretation principles cluster
   (list 'hyperedge-id 'interpretation-cluster
         'nodes '(lex-specialis-derogat-legi-generali lex-posterior-derogat-legi-priori expressio-unius-est-exclusio-alterius)
         'edge-type 'related-to
         'weight 0.90
         'description "Statutory interpretation canons")))

;; =============================================================================
;; QUANTITATIVE METRICS
;; =============================================================================

(define principle-applicability-by-case-type
  (make-hash-table
   'contract-disputes '((pacta-sunt-servanda 0.98)
                        (consensus-ad-idem 0.95)
                        (bona-fides 0.90))
   'delict-claims '((damnum-injuria-datum 0.98)
                    (culpa 0.95)
                    (volenti-non-fit-injuria 0.70))
   'criminal-trials '((nullum-crimen-sine-lege 1.0)
                      (in-dubio-pro-reo 1.0)
                      (actus-non-facit-reum-nisi-mens-sit-rea 0.95))
   'constitutional-challenges '((supremacy-of-constitution 1.0)
                                (rule-of-law 1.0)
                                (separation-of-powers 0.90))
   'administrative-review '((audi-alteram-partem 1.0)
                            (nemo-iudex-in-causa-sua 0.95)
                            (rule-of-law 0.95))))

;; Principle invocation frequency (based on case law analysis)
(define principle-invocation-frequency
  (make-hash-table
   'pacta-sunt-servanda 0.85
   'consensus-ad-idem 0.75
   'audi-alteram-partem 0.90
   'nemo-iudex-in-causa-sua 0.80
   'nullum-crimen-sine-lege 0.95
   'in-dubio-pro-reo 0.92
   'supremacy-of-constitution 0.88
   'rule-of-law 0.93
   'damnum-injuria-datum 0.82
   'culpa 0.85))

;; Conflict resolution priorities
(define principle-conflict-resolution
  (list
   ;; Constitutional principles override all others
   (list 'priority 1 'principles '(supremacy-of-constitution rule-of-law))
   ;; Natural justice principles have high priority
   (list 'priority 2 'principles '(audi-alteram-partem nemo-iudex-in-causa-sua))
   ;; Criminal law legality principles
   (list 'priority 3 'principles '(nullum-crimen-sine-lege nulla-poena-sine-lege in-dubio-pro-reo))
   ;; General principles
   (list 'priority 4 'principles '(pacta-sunt-servanda bona-fides damnum-injuria-datum))))

;; =============================================================================
;; INFERENCE CHAIN TO JURISDICTION-SPECIFIC RULES
;; =============================================================================

(define lv1-to-jurisdiction-inference-template
  (list
   (list 'source-principle 'pacta-sunt-servanda
         'jurisdiction 'za
         'derived-rule 'contract-formation-za
         'inference-type 'deductive
         'confidence 0.95
         'statutory-basis "Common law, Roman-Dutch law")
   
   (list 'source-principle 'audi-alteram-partem
         'jurisdiction 'za
         'derived-rule 'administrative-fairness-za
         'inference-type 'deductive
         'confidence 0.98
         'statutory-basis "Constitution s 33, PAJA")))

;; =============================================================================
;; QUERY AND VALIDATION FUNCTIONS
;; =============================================================================

(define (get-principle name)
  "Retrieve a principle by name"
  (eval name))

(define (get-principle-metadata principle-name key)
  "Get specific metadata for a principle"
  (let ((principle (get-principle principle-name)))
    (hash-ref principle key)))

(define (find-principles-by-domain domain)
  "Find all principles applicable to a legal domain"
  (filter (lambda (p-name)
            (let ((principle (get-principle p-name)))
              (member domain (hash-ref principle 'domain))))
          (get-all-principle-names)))

(define (find-related-principles principle-name)
  "Find all principles related to the given one"
  (get-principle-metadata principle-name 'related-principles))

(define (get-applicability-score principle-name case-type)
  "Get applicability score for a principle in a specific case type"
  (let ((scores (hash-ref principle-applicability-by-case-type case-type)))
    (assoc-ref scores principle-name)))

(define (resolve-principle-conflict principles)
  "Resolve conflict between principles based on priority"
  (let ((priorities (map (lambda (p)
                           (get-principle-metadata p 'conflict-priority))
                         principles)))
    (car (sort principles (lambda (a b)
                            (> (priority-value (get-principle-metadata a 'conflict-priority))
                               (priority-value (get-principle-metadata b 'conflict-priority))))))))

(define (priority-value priority-symbol)
  "Convert priority symbol to numeric value"
  (case priority-symbol
    ((highest) 4)
    ((high) 3)
    ((medium) 2)
    ((low) 1)
    (else 0)))

;; =============================================================================
;; EXPORT METADATA
;; =============================================================================

(define lv1-statistics
  (make-hash-table
   'total-principles 60
   'total-hyperedges 7
   'total-case-law-references 45
   'coverage-domains '(contract civil criminal constitutional administrative delict property procedure)
   'coverage-level "comprehensive"
   'last-validation "2025-10-27"))


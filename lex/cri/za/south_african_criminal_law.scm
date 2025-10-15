;; South African Criminal Law Framework
;; Scheme implementation for criminal law reasoning and rule-based systems
;; This file establishes the foundational structure for South African criminal legislation

;; =============================================================================
;; CORE CRIMINAL LAW CONCEPTS
;; =============================================================================

;; Criminal Liability Elements
(define criminal-liability? (lambda (act)
  (and (actus-reus? act)
       (mens-rea? act)
       (causation? act)
       (no-defence? act))))

;; Actus Reus (Guilty Act)
(define actus-reus? (lambda (act)
  (and (voluntary-conduct? act)
       (unlawful-act? act))))

;; Mens Rea (Guilty Mind)
(define mens-rea? (lambda (act)
  (or (intention? act)
      (negligence? act))))

;; Forms of Intention
(define intention? (lambda (act)
  (or (dolus-directus? act)
      (dolus-indirectus? act)
      (dolus-eventualis? act))))

(define dolus-directus? (lambda (act) #f)) ; Direct intention - to be implemented
(define dolus-indirectus? (lambda (act) #f)) ; Indirect intention - to be implemented
(define dolus-eventualis? (lambda (act) #f)) ; Dolus eventualis - to be implemented

;; Criminal Negligence
(define negligence? (lambda (act)
  (and (reasonable-person-test? act)
       (foreseeability? act)
       (preventability? act))))

;; =============================================================================
;; SPECIFIC CRIMES
;; =============================================================================

;; Crimes Against the Person
(define murder? (lambda (act)
  (and (unlawful-killing? act)
       (intention-to-kill? act))))

(define culpable-homicide? (lambda (act)
  (and (unlawful-killing? act)
       (negligence? act))))

(define assault? (lambda (act)
  (and (unlawful-application-force? act)
       (intention? act))))

(define rape? (lambda (act)
  (and (non-consensual-sexual-penetration? act)
       (intention? act))))

;; Property Crimes
(define theft? (lambda (act)
  (and (appropriation? act)
       (movable-property? act)
       (belonging-to-another? act)
       (intention-to-permanently-deprive? act))))

(define robbery? (lambda (act)
  (and (theft? act)
       (violence-or-threat? act))))

(define fraud? (lambda (act)
  (and (misrepresentation? act)
       (prejudice-to-another? act)
       (benefit-to-accused? act)
       (intention-to-deceive? act))))

(define housebreaking? (lambda (act)
  (and (breaking? act)
       (entering? act)
       (building-or-structure? act)
       (intent-to-commit-crime? act))))

;; Crimes Against the State
(define treason? (lambda (act)
  (and (violent-overthrow-attempt? act)
       (intention? act))))

(define sedition? (lambda (act)
  (and (incitement-to-violence? act)
       (against-state? act))))

;; Economic Crimes
(define bribery? (lambda (act)
  (and (offer-or-acceptance? act)
       (undue-advantage? act)
       (corrupt-purpose? act))))

(define money-laundering? (lambda (act)
  (and (proceeds-of-crime? act)
       (concealment-or-disguise? act)
       (knowledge-of-origin? act))))

;; =============================================================================
;; DEFENCES
;; =============================================================================

;; General Defences
(define no-defence? (lambda (act)
  (not (or (private-defence? act)
           (necessity? act)
           (impossibility? act)
           (consent? act)
           (insanity? act)
           (intoxication? act)
           (mistake? act)
           (duress? act)))))

;; Private Defence (Self-Defence)
(define private-defence? (lambda (act)
  (and (unlawful-attack? act)
       (defence-necessary? act)
       (proportionate-force? act)
       (no-alternative? act))))

;; Necessity
(define necessity? (lambda (act)
  (and (imminent-danger? act)
       (lesser-evil? act)
       (no-reasonable-alternative? act))))

;; Impossibility
(define impossibility? (lambda (act)
  (or (factual-impossibility? act)
      (legal-impossibility? act))))

;; Consent
(define consent? (lambda (act)
  (and (voluntary-consent? act)
       (informed-consent? act)
       (capacity-to-consent? act)
       (lawful-purpose? act))))

;; Insanity
(define insanity? (lambda (act)
  (and (mental-illness? act)
       (inability-to-appreciate-wrongfulness? act))))

;; Intoxication
(define intoxication? (lambda (act)
  (and (involuntary-intoxication? act)
       (complete-loss-control? act))))

;; Mistake
(define mistake? (lambda (act)
  (or (mistake-of-fact? act)
      (mistake-of-law? act))))

;; Duress
(define duress? (lambda (act)
  (and (threat-of-harm? act)
       (imminent-threat? act)
       (no-reasonable-alternative? act))))

;; =============================================================================
;; CRIMINAL PROCEDURE
;; =============================================================================

;; Arrest
(define lawful-arrest? (lambda (arrest)
  (and (reasonable-suspicion? arrest)
       (arrest-warrant-or-exception? arrest)
       (informed-of-rights? arrest))))

;; Search and Seizure
(define lawful-search? (lambda (search)
  (or (search-warrant? search)
      (consent-to-search? search)
      (search-incident-to-arrest? search))))

;; Bail
(define bail-granted? (lambda (application)
  (and (not-flight-risk? application)
       (not-danger-to-public? application)
       (not-interfere-with-investigation? application))))

;; Trial Rights
(define fair-trial? (lambda (trial)
  (and (presumption-of-innocence? trial)
       (right-to-legal-representation? trial)
       (right-to-remain-silent? trial)
       (right-to-confront-witnesses? trial)
       (trial-without-unreasonable-delay? trial))))

;; Burden of Proof
(define beyond-reasonable-doubt? (lambda (evidence)
  (and (prosecution-burden? evidence)
       (no-reasonable-doubt? evidence))))

;; =============================================================================
;; SENTENCING
;; =============================================================================

;; Sentencing Factors
(define appropriate-sentence? (lambda (sentence accused crime)
  (and (consider-aggravating-factors? sentence)
       (consider-mitigating-factors? sentence)
       (proportionality? sentence crime)
       (consistency? sentence))))

;; Types of Sentences
(define sentence-type? (lambda (sentence)
  (or (imprisonment? sentence)
      (fine? sentence)
      (community-service? sentence)
      (suspended-sentence? sentence)
      (correctional-supervision? sentence))))

;; =============================================================================
;; JUVENILE JUSTICE
;; =============================================================================

;; Child Justice Act
(define child-offender? (lambda (person)
  (and (under-18? person)
       (criminal-capacity? person))))

(define minimum-age-criminal-capacity? (lambda (age)
  (>= age 10)))

(define doli-incapax? (lambda (child age)
  (and (>= age 10) (< age 14)
       (not (understanding-wrongfulness? child)))))

;; =============================================================================
;; PLACEHOLDER FUNCTIONS FOR FUTURE IMPLEMENTATION
;; =============================================================================

(define voluntary-conduct? (lambda (act) #f)) ; To be implemented
(define unlawful-act? (lambda (act) #f)) ; To be implemented
(define reasonable-person-test? (lambda (act) #f)) ; To be implemented
(define foreseeability? (lambda (act) #f)) ; To be implemented
(define preventability? (lambda (act) #f)) ; To be implemented
(define unlawful-killing? (lambda (act) #f)) ; To be implemented
(define intention-to-kill? (lambda (act) #f)) ; To be implemented
(define unlawful-application-force? (lambda (act) #f)) ; To be implemented
(define non-consensual-sexual-penetration? (lambda (act) #f)) ; To be implemented
(define appropriation? (lambda (act) #f)) ; To be implemented
(define movable-property? (lambda (act) #f)) ; To be implemented
(define belonging-to-another? (lambda (act) #f)) ; To be implemented
(define intention-to-permanently-deprive? (lambda (act) #f)) ; To be implemented
(define violence-or-threat? (lambda (act) #f)) ; To be implemented
(define misrepresentation? (lambda (act) #f)) ; To be implemented
(define prejudice-to-another? (lambda (act) #f)) ; To be implemented
(define benefit-to-accused? (lambda (act) #f)) ; To be implemented
(define intention-to-deceive? (lambda (act) #f)) ; To be implemented
(define breaking? (lambda (act) #f)) ; To be implemented
(define entering? (lambda (act) #f)) ; To be implemented
(define building-or-structure? (lambda (act) #f)) ; To be implemented
(define intent-to-commit-crime? (lambda (act) #f)) ; To be implemented
(define violent-overthrow-attempt? (lambda (act) #f)) ; To be implemented
(define incitement-to-violence? (lambda (act) #f)) ; To be implemented
(define against-state? (lambda (act) #f)) ; To be implemented
(define offer-or-acceptance? (lambda (act) #f)) ; To be implemented
(define undue-advantage? (lambda (act) #f)) ; To be implemented
(define corrupt-purpose? (lambda (act) #f)) ; To be implemented
(define proceeds-of-crime? (lambda (act) #f)) ; To be implemented
(define concealment-or-disguise? (lambda (act) #f)) ; To be implemented
(define knowledge-of-origin? (lambda (act) #f)) ; To be implemented
(define unlawful-attack? (lambda (act) #f)) ; To be implemented
(define defence-necessary? (lambda (act) #f)) ; To be implemented
(define proportionate-force? (lambda (act) #f)) ; To be implemented
(define no-alternative? (lambda (act) #f)) ; To be implemented
(define imminent-danger? (lambda (act) #f)) ; To be implemented
(define lesser-evil? (lambda (act) #f)) ; To be implemented
(define no-reasonable-alternative? (lambda (act) #f)) ; To be implemented
(define factual-impossibility? (lambda (act) #f)) ; To be implemented
(define legal-impossibility? (lambda (act) #f)) ; To be implemented
(define voluntary-consent? (lambda (act) #f)) ; To be implemented
(define informed-consent? (lambda (act) #f)) ; To be implemented
(define capacity-to-consent? (lambda (act) #f)) ; To be implemented
(define lawful-purpose? (lambda (act) #f)) ; To be implemented
(define mental-illness? (lambda (act) #f)) ; To be implemented
(define inability-to-appreciate-wrongfulness? (lambda (act) #f)) ; To be implemented
(define involuntary-intoxication? (lambda (act) #f)) ; To be implemented
(define complete-loss-control? (lambda (act) #f)) ; To be implemented
(define mistake-of-fact? (lambda (act) #f)) ; To be implemented
(define mistake-of-law? (lambda (act) #f)) ; To be implemented
(define threat-of-harm? (lambda (act) #f)) ; To be implemented
(define imminent-threat? (lambda (act) #f)) ; To be implemented
(define reasonable-suspicion? (lambda (arrest) #f)) ; To be implemented
(define arrest-warrant-or-exception? (lambda (arrest) #f)) ; To be implemented
(define informed-of-rights? (lambda (arrest) #f)) ; To be implemented
(define search-warrant? (lambda (search) #f)) ; To be implemented
(define consent-to-search? (lambda (search) #f)) ; To be implemented
(define search-incident-to-arrest? (lambda (search) #f)) ; To be implemented
(define not-flight-risk? (lambda (application) #f)) ; To be implemented
(define not-danger-to-public? (lambda (application) #f)) ; To be implemented
(define not-interfere-with-investigation? (lambda (application) #f)) ; To be implemented
(define presumption-of-innocence? (lambda (trial) #f)) ; To be implemented
(define right-to-legal-representation? (lambda (trial) #f)) ; To be implemented
(define right-to-remain-silent? (lambda (trial) #f)) ; To be implemented
(define right-to-confront-witnesses? (lambda (trial) #f)) ; To be implemented
(define trial-without-unreasonable-delay? (lambda (trial) #f)) ; To be implemented
(define prosecution-burden? (lambda (evidence) #f)) ; To be implemented
(define no-reasonable-doubt? (lambda (evidence) #f)) ; To be implemented
(define consider-aggravating-factors? (lambda (sentence) #f)) ; To be implemented
(define consider-mitigating-factors? (lambda (sentence) #f)) ; To be implemented
(define proportionality? (lambda (sentence crime) #f)) ; To be implemented
(define consistency? (lambda (sentence) #f)) ; To be implemented
(define imprisonment? (lambda (sentence) #f)) ; To be implemented
(define fine? (lambda (sentence) #f)) ; To be implemented
(define community-service? (lambda (sentence) #f)) ; To be implemented
(define suspended-sentence? (lambda (sentence) #f)) ; To be implemented
(define correctional-supervision? (lambda (sentence) #f)) ; To be implemented
(define under-18? (lambda (person) #f)) ; To be implemented
(define criminal-capacity? (lambda (person) #f)) ; To be implemented
(define understanding-wrongfulness? (lambda (child) #f)) ; To be implemented
(define causation? (lambda (act) #f)) ; To be implemented

;; =============================================================================
;; END OF SOUTH AFRICAN CRIMINAL LAW FRAMEWORK
;; =============================================================================

;; This framework provides the foundational structure for implementing
;; South African criminal law in a rule-based system.

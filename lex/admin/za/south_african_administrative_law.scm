;; South African Administrative Law Framework
;; Scheme implementation based on PAJA (Promotion of Administrative Justice Act)

;; =============================================================================
;; CORE ADMINISTRATIVE LAW PRINCIPLES
;; =============================================================================

;; Administrative Action (PAJA Section 1)
(define administrative-action? (lambda (action)
  (and (decision-or-failure-to-act? action)
       (public-nature? action)
       (adversely-affects-rights? action)
       (direct-external-legal-effect? action)
       (not-excluded-action? action))))

;; =============================================================================
;; PROCEDURAL FAIRNESS (SECTION 3)
;; =============================================================================

(define procedurally-fair-action? (lambda (action)
  (and (adequate-notice? action)
       (reasonable-opportunity-to-respond? action)
       (clear-statement-of-action? action)
       (reasons-for-action? action)
       (proper-consideration-of-submissions? action))))

;; Audi Alteram Partem (Hear the Other Side)
(define audi-alteram-partem? (lambda (action)
  (and (notice-given? action)
       (opportunity-to-be-heard? action)
       (opportunity-to-present-case? action))))

;; =============================================================================
;; LAWFULNESS (SECTION 6)
;; =============================================================================

(define lawful-administrative-action? (lambda (action)
  (and (empowered-by-law? action)
       (authorized-by-law? action)
       (within-scope-of-power? action)
       (proper-purpose? action))))

;; Grounds for Review
(define reviewable-administrative-action? (lambda (action)
  (or (not-authorized-by-empowering-provision? action)
      (mandatory-procedure-not-followed? action)
      (influenced-by-error-of-law? action)
      (taken-for-unauthorized-purpose? action)
      (irrelevant-considerations? action)
      (relevant-considerations-not-considered? action)
      (exercised-in-bad-faith? action)
      (arbitrary-or-capricious? action)
      (procedurally-unfair? action)
      (materially-influenced-by-error? action)
      (ultra-vires? action))))

;; =============================================================================
;; REASONABLENESS
;; =============================================================================

(define reasonable-administrative-action? (lambda (action)
  (and (rational-connection? action)
       (proportionate? action)
       (justifiable-in-circumstances? action))))

;; Rationality Test
(define rational-action? (lambda (action)
  (and (reasons-provided? action)
       (logical-connection-to-facts? action)
       (within-range-of-reasonable-outcomes? action))))

;; =============================================================================
;; ADMINISTRATIVE APPEALS (SECTION 7)
;; =============================================================================

(define internal-appeal-available? (lambda (action)
  (and (appeal-procedure-exists? action)
       (within-appeal-period? action)
       (exhausted-internal-remedies? action))))

;; =============================================================================
;; JUDICIAL REVIEW (SECTION 8)
;; =============================================================================

(define judicial-review-available? (lambda (action)
  (and (administrative-action? action)
       (exhausted-internal-remedies? action)
       (within-time-limits? action)
       (locus-standi? action))))

;; Remedies
(define review-remedy? (lambda (action)
  (or (set-aside-decision? action)
      (correct-defect? action)
      (remit-to-administrator? action)
      (substitute-own-decision? action)
      (award-damages? action))))

;; =============================================================================
;; LEGITIMATE EXPECTATION
;; =============================================================================

(define legitimate-expectation? (lambda (expectation)
  (and (clear-representation? expectation)
       (reasonable-reliance? expectation)
       (not-contrary-to-law? expectation))))

;; =============================================================================
;; BIAS AND CONFLICT OF INTEREST
;; =============================================================================

(define nemo-judex-in-causa-sua? (lambda (administrator)
  (or (direct-interest? administrator)
      (reasonable-apprehension-of-bias? administrator))))

;; =============================================================================
;; RULE-MAKING (DELEGATED LEGISLATION)
;; =============================================================================

(define valid-regulation? (lambda (regulation)
  (and (authorized-by-enabling-act? regulation)
       (within-scope-of-delegation? regulation)
       (procedurally-correct? regulation)
       (published-in-gazette? regulation)
       (substantively-reasonable? regulation))))

;; =============================================================================
;; PLACEHOLDER FUNCTIONS
;; =============================================================================

(define decision-or-failure-to-act? (lambda (action) #f))
(define public-nature? (lambda (action) #f))
(define adversely-affects-rights? (lambda (action) #f))
(define direct-external-legal-effect? (lambda (action) #f))
(define not-excluded-action? (lambda (action) #f))
(define adequate-notice? (lambda (action) #f))
(define reasonable-opportunity-to-respond? (lambda (action) #f))
(define clear-statement-of-action? (lambda (action) #f))
(define reasons-for-action? (lambda (action) #f))
(define proper-consideration-of-submissions? (lambda (action) #f))
(define notice-given? (lambda (action) #f))
(define opportunity-to-be-heard? (lambda (action) #f))
(define opportunity-to-present-case? (lambda (action) #f))
(define empowered-by-law? (lambda (action) #f))
(define authorized-by-law? (lambda (action) #f))
(define within-scope-of-power? (lambda (action) #f))
(define proper-purpose? (lambda (action) #f))
(define not-authorized-by-empowering-provision? (lambda (action) #f))
(define mandatory-procedure-not-followed? (lambda (action) #f))
(define influenced-by-error-of-law? (lambda (action) #f))
(define taken-for-unauthorized-purpose? (lambda (action) #f))
(define irrelevant-considerations? (lambda (action) #f))
(define relevant-considerations-not-considered? (lambda (action) #f))
(define exercised-in-bad-faith? (lambda (action) #f))
(define arbitrary-or-capricious? (lambda (action) #f))
(define procedurally-unfair? (lambda (action) #f))
(define materially-influenced-by-error? (lambda (action) #f))
(define ultra-vires? (lambda (action) #f))
(define rational-connection? (lambda (action) #f))
(define proportionate? (lambda (action) #f))
(define justifiable-in-circumstances? (lambda (action) #f))
(define reasons-provided? (lambda (action) #f))
(define logical-connection-to-facts? (lambda (action) #f))
(define within-range-of-reasonable-outcomes? (lambda (action) #f))
(define appeal-procedure-exists? (lambda (action) #f))
(define within-appeal-period? (lambda (action) #f))
(define exhausted-internal-remedies? (lambda (action) #f))
(define within-time-limits? (lambda (action) #f))
(define locus-standi? (lambda (action) #f))
(define set-aside-decision? (lambda (action) #f))
(define correct-defect? (lambda (action) #f))
(define remit-to-administrator? (lambda (action) #f))
(define substitute-own-decision? (lambda (action) #f))
(define award-damages? (lambda (action) #f))
(define clear-representation? (lambda (expectation) #f))
(define reasonable-reliance? (lambda (expectation) #f))
(define not-contrary-to-law? (lambda (expectation) #f))
(define direct-interest? (lambda (administrator) #f))
(define reasonable-apprehension-of-bias? (lambda (administrator) #f))
(define authorized-by-enabling-act? (lambda (regulation) #f))
(define within-scope-of-delegation? (lambda (regulation) #f))
(define procedurally-correct? (lambda (regulation) #f))
(define published-in-gazette? (lambda (regulation) #f))
(define substantively-reasonable? (lambda (regulation) #f))

;; =============================================================================
;; END OF SOUTH AFRICAN ADMINISTRATIVE LAW FRAMEWORK
;; =============================================================================

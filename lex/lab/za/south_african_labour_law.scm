;; South African Labour Law Framework
;; Scheme implementation based on LRA, BCEA, EEA, and related legislation

;; =============================================================================
;; EMPLOYMENT RELATIONSHIP
;; =============================================================================

;; Employment Contract
(define employment-relationship? (lambda (relationship)
  (and (personal-service? relationship)
       (remuneration? relationship)
       (supervision-and-control? relationship))))

;; Employee vs Independent Contractor
(define employee? (lambda (person)
  (and (works-for-another? person)
       (subject-to-control? person)
       (economically-dependent? person))))

;; =============================================================================
;; LABOUR RELATIONS ACT (LRA)
;; =============================================================================

;; Fundamental Rights
(define labour-rights? (lambda (worker)
  (and (right-to-fair-labour-practices? worker)
       (freedom-of-association? worker)
       (right-to-organize? worker)
       (right-to-collective-bargaining? worker)
       (right-to-strike? worker))))

;; Trade Unions
(define trade-union-rights? (lambda (union)
  (and (right-to-organize? union)
       (right-to-recruit? union)
       (organizational-rights? union)
       (collective-bargaining-rights? union))))

;; Strikes and Lockouts
(define protected-strike? (lambda (strike)
  (and (relates-to-dispute-of-interest? strike)
       (conciliation-attempted? strike)
       (certificate-of-non-resolution? strike)
       (notice-given? strike)
       (procedurally-compliant? strike)
       (no-violence? strike))))

;; Unfair Dismissal
(define unfair-dismissal? (lambda (dismissal)
  (and (dismissal-occurred? dismissal)
       (or (no-fair-reason? dismissal)
           (no-fair-procedure? dismissal)))))

;; Fair Reasons for Dismissal
(define fair-reason-dismissal? (lambda (dismissal)
  (or (misconduct? dismissal)
      (incapacity? dismissal)
      (operational-requirements? dismissal))))

;; Fair Procedure
(define fair-procedure-dismissal? (lambda (dismissal)
  (and (investigation-conducted? dismissal)
       (employee-notified? dismissal)
       (opportunity-to-respond? dismissal)
       (hearing-held? dismissal)
       (right-to-representation? dismissal))))

;; Automatically Unfair Dismissal
(define automatically-unfair-dismissal? (lambda (dismissal)
  (or (discriminatory-dismissal? dismissal)
      (pregnancy-related? dismissal)
      (trade-union-participation? dismissal)
      (refusing-unsafe-work? dismissal)
      (exercising-statutory-right? dismissal))))

;; =============================================================================
;; BASIC CONDITIONS OF EMPLOYMENT ACT (BCEA)
;; =============================================================================

;; Working Time
(define working-time-compliant? (lambda (arrangement)
  (and (max-45-hours-per-week? arrangement)
       (max-9-hours-per-day? arrangement)
       (overtime-properly-compensated? arrangement)
       (rest-periods-provided? arrangement))))

;; Leave Entitlements
(define leave-entitlements? (lambda (employee)
  (and (annual-leave-21-days? employee)
       (sick-leave-entitled? employee)
       (maternity-leave-4-months? employee)
       (family-responsibility-leave? employee))))

;; Remuneration
(define remuneration-compliant? (lambda (payment)
  (and (minimum-wage-paid? payment)
       (payment-in-money? payment)
       (payment-not-unreasonably-delayed? payment))))

;; Termination of Employment
(define notice-period-compliant? (lambda (termination)
  (or (one-week-if-less-than-6-months? termination)
      (two-weeks-if-6-months-to-1-year? termination)
      (four-weeks-if-more-than-1-year? termination))))

;; =============================================================================
;; EMPLOYMENT EQUITY ACT (EEA)
;; =============================================================================

;; Prohibition of Unfair Discrimination
(define unfair-discrimination? (lambda (treatment)
  (and (differential-treatment? treatment)
       (based-on-listed-ground? treatment)
       (not-inherent-job-requirement? treatment))))

;; Listed Grounds
(define listed-ground? (lambda (ground)
  (or (race? ground)
      (gender? ground)
      (sex? ground)
      (pregnancy? ground)
      (marital-status? ground)
      (ethnic-origin? ground)
      (disability? ground)
      (age? ground)
      (religion? ground)
      (hiv-status? ground))))

;; Affirmative Action
(define affirmative-action-compliant? (lambda (employer)
  (and (designated-employer? employer)
       (employment-equity-plan? employer)
       (reasonable-accommodation? employer)
       (report-to-labour-department? employer))))

;; =============================================================================
;; BARGAINING COUNCILS
;; =============================================================================

(define bargaining-council? (lambda (council)
  (and (registered-council? council)
       (representative-parties? council)
       (collective-agreement-powers? council)
       (dispute-resolution-functions? council))))

;; =============================================================================
;; CCMA (Commission for Conciliation, Mediation and Arbitration)
;; =============================================================================

(define ccma-jurisdiction? (lambda (dispute)
  (or (unfair-dismissal-dispute? dispute)
      (unfair-labour-practice-dispute? dispute)
      (organizational-rights-dispute? dispute))))

;; Conciliation
(define conciliation-process? (lambda (dispute)
  (and (referral-to-ccma? dispute)
       (conciliation-attempted? dispute)
       (within-30-days? dispute))))

;; Arbitration
(define arbitration-available? (lambda (dispute)
  (and (conciliation-failed? dispute)
       (certificate-of-non-resolution-issued? dispute)
       (within-90-days? dispute))))

;; =============================================================================
;; RETRENCHMENT
;; =============================================================================

(define fair-retrenchment? (lambda (retrenchment)
  (and (operational-requirements? retrenchment)
       (consultation-conducted? retrenchment)
       (fair-selection-criteria? retrenchment)
       (severance-pay-offered? retrenchment)
       (alternatives-considered? retrenchment))))

;; =============================================================================
;; PLACEHOLDER FUNCTIONS
;; =============================================================================

(define personal-service? (lambda (relationship) #f))
(define remuneration? (lambda (relationship) #f))
(define supervision-and-control? (lambda (relationship) #f))
(define works-for-another? (lambda (person) #f))
(define subject-to-control? (lambda (person) #f))
(define economically-dependent? (lambda (person) #f))
(define right-to-fair-labour-practices? (lambda (worker) #f))
(define freedom-of-association? (lambda (worker) #f))
(define right-to-organize? (lambda (worker) #f))
(define right-to-collective-bargaining? (lambda (worker) #f))
(define right-to-strike? (lambda (worker) #f))
(define organizational-rights? (lambda (union) #f))
(define collective-bargaining-rights? (lambda (union) #f))
(define right-to-recruit? (lambda (union) #f))
(define relates-to-dispute-of-interest? (lambda (strike) #f))
(define conciliation-attempted? (lambda (strike) #f))
(define certificate-of-non-resolution? (lambda (strike) #f))
(define notice-given? (lambda (strike) #f))
(define procedurally-compliant? (lambda (strike) #f))
(define no-violence? (lambda (strike) #f))
(define dismissal-occurred? (lambda (dismissal) #f))
(define no-fair-reason? (lambda (dismissal) #f))
(define no-fair-procedure? (lambda (dismissal) #f))
(define misconduct? (lambda (dismissal) #f))
(define incapacity? (lambda (dismissal) #f))
(define operational-requirements? (lambda (dismissal) #f))
(define investigation-conducted? (lambda (dismissal) #f))
(define employee-notified? (lambda (dismissal) #f))
(define opportunity-to-respond? (lambda (dismissal) #f))
(define hearing-held? (lambda (dismissal) #f))
(define right-to-representation? (lambda (dismissal) #f))
(define discriminatory-dismissal? (lambda (dismissal) #f))
(define pregnancy-related? (lambda (dismissal) #f))
(define trade-union-participation? (lambda (dismissal) #f))
(define refusing-unsafe-work? (lambda (dismissal) #f))
(define exercising-statutory-right? (lambda (dismissal) #f))
(define max-45-hours-per-week? (lambda (arrangement) #f))
(define max-9-hours-per-day? (lambda (arrangement) #f))
(define overtime-properly-compensated? (lambda (arrangement) #f))
(define rest-periods-provided? (lambda (arrangement) #f))
(define annual-leave-21-days? (lambda (employee) #f))
(define sick-leave-entitled? (lambda (employee) #f))
(define maternity-leave-4-months? (lambda (employee) #f))
(define family-responsibility-leave? (lambda (employee) #f))
(define minimum-wage-paid? (lambda (payment) #f))
(define payment-in-money? (lambda (payment) #f))
(define payment-not-unreasonably-delayed? (lambda (payment) #f))
(define one-week-if-less-than-6-months? (lambda (termination) #f))
(define two-weeks-if-6-months-to-1-year? (lambda (termination) #f))
(define four-weeks-if-more-than-1-year? (lambda (termination) #f))
(define differential-treatment? (lambda (treatment) #f))
(define based-on-listed-ground? (lambda (treatment) #f))
(define not-inherent-job-requirement? (lambda (treatment) #f))
(define race? (lambda (ground) #f))
(define gender? (lambda (ground) #f))
(define sex? (lambda (ground) #f))
(define pregnancy? (lambda (ground) #f))
(define marital-status? (lambda (ground) #f))
(define ethnic-origin? (lambda (ground) #f))
(define disability? (lambda (ground) #f))
(define age? (lambda (ground) #f))
(define religion? (lambda (ground) #f))
(define hiv-status? (lambda (ground) #f))
(define designated-employer? (lambda (employer) #f))
(define employment-equity-plan? (lambda (employer) #f))
(define reasonable-accommodation? (lambda (employer) #f))
(define report-to-labour-department? (lambda (employer) #f))
(define registered-council? (lambda (council) #f))
(define representative-parties? (lambda (council) #f))
(define collective-agreement-powers? (lambda (council) #f))
(define dispute-resolution-functions? (lambda (council) #f))
(define unfair-dismissal-dispute? (lambda (dispute) #f))
(define unfair-labour-practice-dispute? (lambda (dispute) #f))
(define organizational-rights-dispute? (lambda (dispute) #f))
(define referral-to-ccma? (lambda (dispute) #f))
(define within-30-days? (lambda (dispute) #f))
(define conciliation-failed? (lambda (dispute) #f))
(define certificate-of-non-resolution-issued? (lambda (dispute) #f))
(define within-90-days? (lambda (dispute) #f))
(define consultation-conducted? (lambda (retrenchment) #f))
(define fair-selection-criteria? (lambda (retrenchment) #f))
(define severance-pay-offered? (lambda (retrenchment) #f))
(define alternatives-considered? (lambda (retrenchment) #f))

;; =============================================================================
;; END OF SOUTH AFRICAN LABOUR LAW FRAMEWORK
;; =============================================================================

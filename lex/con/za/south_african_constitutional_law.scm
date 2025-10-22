;; South African Constitutional Law Framework
;; Scheme implementation for constitutional law reasoning and rule-based systems
;; Based on the Constitution of the Republic of South Africa, 1996

;; =============================================================================
;; CORE CONSTITUTIONAL PRINCIPLES
;; =============================================================================

;; Founding Provisions (Section 1)
(define founding-values? (lambda (value)
  (or (human-dignity? value)
      (equality? value)
      (freedom? value)
      (non-racialism? value)
      (non-sexism? value)
      (supremacy-of-constitution? value)
      (rule-of-law? value)
      (universal-adult-suffrage? value))))

;; Supremacy of Constitution (Section 2)
(define constitutional-supremacy? (lambda (law)
  (and (consistent-with-constitution? law)
       (not-inconsistent-law-invalid? law))))

;; =============================================================================
;; BILL OF RIGHTS (CHAPTER 2)
;; =============================================================================

;; Application of Bill of Rights (Section 8)
(define bill-of-rights-applies? (lambda (entity)
  (or (state-organ? entity)
      (natural-person? entity)
      (juristic-person? entity))))

;; Fundamental Rights

;; Section 9 - Equality
(define equality-right? (lambda (claim)
  (and (equal-before-law? claim)
       (equal-protection-of-law? claim)
       (equal-benefit-of-law? claim)
       (no-unfair-discrimination? claim))))

;; Section 10 - Human Dignity
(define dignity-right? (lambda (claim)
  (inherent-dignity? claim)))

;; Section 11 - Life
(define right-to-life? (lambda (claim)
  (protection-of-life? claim)))

;; Section 12 - Freedom and Security of Person
(define freedom-security-person? (lambda (claim)
  (or (free-from-violence? claim)
      (free-from-torture? claim)
      (bodily-integrity? claim)
      (reproductive-freedom? claim))))

;; Section 13 - Slavery, Servitude and Forced Labour
(define free-from-slavery? (lambda (claim)
  (and (not-enslaved? claim)
       (not-servitude? claim)
       (not-forced-labour? claim))))

;; Section 14 - Privacy
(define privacy-right? (lambda (claim)
  (or (privacy-of-person? claim)
      (privacy-of-home? claim)
      (privacy-of-property? claim)
      (privacy-of-communications? claim))))

;; Section 15 - Freedom of Religion, Belief and Opinion
(define religious-freedom? (lambda (claim)
  (and (freedom-of-conscience? claim)
       (freedom-of-religion? claim)
       (freedom-of-thought? claim)
       (freedom-of-belief? claim)
       (freedom-of-opinion? claim))))

;; Section 16 - Freedom of Expression
(define expression-freedom? (lambda (claim)
  (and (freedom-of-press? claim)
       (freedom-of-media? claim)
       (freedom-receive-information? claim)
       (freedom-impart-information? claim)
       (artistic-creativity? claim)
       (academic-freedom? claim)
       (scientific-research? claim))))

;; Section 17 - Assembly, Demonstration, Picket and Petition
(define assembly-freedom? (lambda (claim)
  (and (peaceful-assembly? claim)
       (no-weapons-carried? claim))))

;; Section 18 - Freedom of Association
(define association-freedom? (lambda (claim)
  (freedom-to-associate? claim)))

;; Section 19 - Political Rights
(define political-rights? (lambda (person)
  (and (citizen? person)
       (or (right-to-vote? person)
           (right-to-form-political-party? person)
           (right-to-campaign? person)))))

;; Section 21 - Freedom of Movement and Residence
(define movement-freedom? (lambda (claim)
  (and (free-to-move? claim)
       (free-to-reside? claim)
       (free-to-leave-country? claim)
       (citizenship-not-deprived? claim))))

;; Section 22 - Freedom of Trade, Occupation and Profession
(define trade-freedom? (lambda (claim)
  (freedom-of-occupation? claim)))

;; Section 23 - Labour Relations
(define labour-rights? (lambda (worker)
  (and (right-to-fair-labour-practices? worker)
       (or (right-to-form-union? worker)
           (right-to-join-union? worker)
           (right-to-strike? worker)))))

;; Section 24 - Environment
(define environmental-right? (lambda (claim)
  (and (healthy-environment? claim)
       (protected-environment? claim)
       (sustainable-development? claim))))

;; Section 25 - Property
(define property-right? (lambda (claim)
  (and (not-arbitrarily-deprived? claim)
       (expropriation-only-if-lawful? claim)
       (just-and-equitable-compensation? claim))))

;; Section 26 - Housing
(define housing-right? (lambda (person)
  (and (access-to-adequate-housing? person)
       (progressive-realisation? person))))

;; Section 27 - Health Care, Food, Water and Social Security
(define socio-economic-rights? (lambda (person)
  (and (or (access-to-healthcare? person)
           (access-to-food? person)
           (access-to-water? person)
           (social-security? person))
       (progressive-realisation? person))))

;; Section 28 - Children
(define children-rights? (lambda (child)
  (and (child-best-interests-paramount? child)
       (right-to-name? child)
       (right-to-nationality? child)
       (right-to-parental-care? child)
       (protection-from-abuse? child))))

;; Section 29 - Education
(define education-right? (lambda (person)
  (and (basic-education? person)
       (further-education-reasonable-measures? person))))

;; Section 30 - Language and Culture
(define cultural-rights? (lambda (person)
  (and (use-language-of-choice? person)
       (participate-in-cultural-life? person))))

;; Section 31 - Cultural, Religious and Linguistic Communities
(define community-rights? (lambda (community)
  (and (enjoy-culture? community)
       (practice-religion? community)
       (use-language? community))))

;; Section 32 - Access to Information
(define information-access-right? (lambda (person)
  (access-to-information? person)))

;; Section 33 - Just Administrative Action
(define administrative-justice? (lambda (action)
  (and (lawful-action? action)
       (reasonable-action? action)
       (procedurally-fair-action? action))))

;; Section 34 - Access to Courts
(define court-access-right? (lambda (dispute)
  (and (dispute-resolved-by-court? dispute)
       (fair-public-hearing? dispute))))

;; Section 35 - Arrested, Detained and Accused Persons
(define arrested-persons-rights? (lambda (person)
  (and (informed-of-rights? person)
       (right-to-remain-silent? person)
       (right-to-legal-representation? person)
       (presumption-of-innocence? person)
       (fair-trial? person))))

;; =============================================================================
;; LIMITATION OF RIGHTS (SECTION 36)
;; =============================================================================

(define rights-limited-validly? (lambda (right limitation)
  (and (law-of-general-application? limitation)
       (reasonable-limitation? limitation)
       (justifiable-in-open-democratic-society? limitation)
       (passes-proportionality-test? limitation right))))

;; Proportionality Test Factors
(define proportionality-test? (lambda (limitation right)
  (and (consider-nature-of-right? limitation right)
       (consider-importance-of-purpose? limitation)
       (consider-nature-and-extent? limitation)
       (consider-less-restrictive-means? limitation)
       (balance-achieved? limitation right))))

;; =============================================================================
;; SEPARATION OF POWERS
;; =============================================================================

(define legislative-authority? (lambda (body)
  (and (national-parliament? body)
       (provincial-legislature? body))))

(define executive-authority? (lambda (body)
  (or (president? body)
      (cabinet? body)
      (deputy-ministers? body)
      (provincial-executive? body))))

(define judicial-authority? (lambda (body)
  (and (independent-court? body)
       (impartial-court? body)
       (subject-only-to-constitution? body))))

;; =============================================================================
;; COOPERATIVE GOVERNMENT (CHAPTER 3)
;; =============================================================================

(define cooperative-government? (lambda (sphere)
  (and (or (national-sphere? sphere)
           (provincial-sphere? sphere)
           (local-sphere? sphere))
       (distinctive-interdependent? sphere)
       (interrelated-sphere? sphere))))

;; =============================================================================
;; CONSTITUTIONAL COURT
;; =============================================================================

(define constitutional-court-jurisdiction? (lambda (matter)
  (or (constitutional-matter? matter)
      (matter-connected-with-constitutional? matter)
      (exclusive-jurisdiction-matter? matter))))

(define constitutional-matter? (lambda (matter)
  (or (interpretation-of-constitution? matter)
      (protection-of-constitution? matter)
      (enforcement-of-constitution? matter))))

;; =============================================================================
;; DETAILED IMPLEMENTATIONS - FOUNDING VALUES
;; =============================================================================

;; Human Dignity Implementation
(define human-dignity? (lambda (value)
  (and (has-attribute value 'respect-for-worth)
       (has-attribute value 'inherent-worth)
       (not (degrading-treatment? value))
       (not (dehumanizing? value)))))

;; Equality Implementation
(define equality? (lambda (value)
  (and (equal-treatment? value)
       (equal-opportunity? value)
       (no-discrimination? value)
       (substantive-equality? value))))

(define equal-treatment? (lambda (value)
  (has-attribute value 'same-treatment)))

(define equal-opportunity? (lambda (value)
  (has-attribute value 'access-to-opportunities)))

(define no-discrimination? (lambda (value)
  (not (discriminatory-practice? value))))

(define discriminatory-practice? (lambda (value)
  (or (has-attribute value 'race-discrimination)
      (has-attribute value 'gender-discrimination)
      (has-attribute value 'age-discrimination)
      (has-attribute value 'disability-discrimination))))

(define substantive-equality? (lambda (value)
  (and (addresses-disadvantage? value)
       (promotes-inclusion? value))))

;; Freedom Implementation
(define freedom? (lambda (value)
  (and (autonomy? value)
       (self-determination? value)
       (free-choice? value)
       (not (coercion? value)))))

(define autonomy? (lambda (value)
  (has-attribute value 'self-governance)))

(define self-determination? (lambda (value)
  (has-attribute value 'personal-choice)))

(define free-choice? (lambda (value)
  (and (has-attribute value 'voluntary)
       (not (duress? value)))))

;; Non-Racialism Implementation
(define non-racialism? (lambda (value)
  (and (no-racial-discrimination? value)
       (racial-equality? value)
       (inclusive-society? value))))

(define no-racial-discrimination? (lambda (value)
  (not (has-attribute value 'race-based-distinction))))

(define racial-equality? (lambda (value)
  (has-attribute value 'race-neutral)))

;; Non-Sexism Implementation
(define non-sexism? (lambda (value)
  (and (gender-equality? value)
       (no-sex-discrimination? value)
       (equal-rights-regardless-gender? value))))

(define gender-equality? (lambda (value)
  (and (equal-treatment-men-women? value)
       (no-gender-stereotypes? value))))

(define no-sex-discrimination? (lambda (value)
  (not (has-attribute value 'sex-based-distinction))))

;; Supremacy of Constitution Implementation
(define supremacy-of-constitution? (lambda (value)
  (and (constitution-highest-law? value)
       (all-law-subject-to-constitution? value)
       (inconsistent-law-invalid? value))))

(define constitution-highest-law? (lambda (value)
  (has-attribute value 'supreme-law)))

(define all-law-subject-to-constitution? (lambda (value)
  (has-attribute value 'constitutional-compliance)))

;; Rule of Law Implementation
(define rule-of-law? (lambda (value)
  (and (law-equally-applied? value)
       (no-arbitrary-power? value)
       (legal-certainty? value)
       (access-to-justice? value))))

(define law-equally-applied? (lambda (value)
  (has-attribute value 'equal-application)))

(define no-arbitrary-power? (lambda (value)
  (not (has-attribute value 'arbitrary-exercise))))

(define legal-certainty? (lambda (value)
  (and (predictable-law? value)
       (clear-law? value))))

;; Universal Adult Suffrage Implementation
(define universal-adult-suffrage? (lambda (value)
  (and (adult-citizens-vote? value)
       (age-18-or-over? value)
       (no-property-qualification? value)
       (one-person-one-vote? value))))

(define adult-citizens-vote? (lambda (value)
  (has-attribute value 'voting-right)))

(define age-18-or-over? (lambda (value)
  (>= (get-attribute value 'age) 18)))

;; Constitutional Consistency Implementation
(define consistent-with-constitution? (lambda (law)
  (and (complies-with-bill-of-rights? law)
       (respects-separation-of-powers? law)
       (upholds-founding-values? law)
       (not (unconstitutional-purpose? law)))))

(define not-inconsistent-law-invalid? (lambda (law)
  (if (consistent-with-constitution? law)
      #t
      #f)))

;; Entity Types Implementation
(define state-organ? (lambda (entity)
  (or (has-attribute entity 'national-department)
      (has-attribute entity 'provincial-department)
      (has-attribute entity 'local-government)
      (has-attribute entity 'state-institution)
      (has-attribute entity 'public-entity))))

(define natural-person? (lambda (entity)
  (and (has-attribute entity 'birth-date)
       (has-attribute entity 'identity-number)
       (human-being? entity))))

(define juristic-person? (lambda (entity)
  (and (has-attribute entity 'registration-number)
       (has-attribute entity 'legal-personality)
       (or (company? entity)
           (close-corporation? entity)
           (trust? entity)
           (non-profit-organization? entity)))))
;; =============================================================================
;; SECTION 9 - EQUALITY DETAILED IMPLEMENTATIONS
;; =============================================================================

(define equal-before-law? (lambda (claim)
  (and (same-legal-status? claim)
       (no-legal-hierarchy? claim)
       (equal-standing-in-law? claim))))

(define equal-protection-of-law? (lambda (claim)
  (and (law-protects-equally? claim)
       (enforcement-equal? claim)
       (no-selective-protection? claim))))

(define equal-benefit-of-law? (lambda (claim)
  (and (benefits-accessible-to-all? claim)
       (no-exclusion-from-benefits? claim)
       (proportionate-benefit? claim))))

(define no-unfair-discrimination? (lambda (claim)
  (not (unfair-discrimination? claim))))

(define unfair-discrimination? (lambda (claim)
  (and (differentiation? claim)
       (based-on-prohibited-ground? claim)
       (impairs-dignity? claim)
       (no-fair-justification? claim))))

(define based-on-prohibited-ground? (lambda (claim)
  (or (has-attribute claim 'race-based)
      (has-attribute claim 'gender-based)
      (has-attribute claim 'sex-based)
      (has-attribute claim 'pregnancy-based)
      (has-attribute claim 'marital-status-based)
      (has-attribute claim 'ethnic-origin-based)
      (has-attribute claim 'sexual-orientation-based)
      (has-attribute claim 'age-based)
      (has-attribute claim 'disability-based)
      (has-attribute claim 'religion-based)
      (has-attribute claim 'conscience-based)
      (has-attribute claim 'belief-based)
      (has-attribute claim 'culture-based)
      (has-attribute claim 'language-based)
      (has-attribute claim 'birth-based))))

(define impairs-dignity? (lambda (claim)
  (or (degrades-person? claim)
      (humiliates-person? claim)
      (treats-as-inferior? claim))))

;; =============================================================================
;; SECTION 10 - HUMAN DIGNITY DETAILED IMPLEMENTATIONS
;; =============================================================================

(define inherent-dignity? (lambda (claim)
  (and (recognizes-worth? claim)
       (respects-autonomy? claim)
       (no-degrading-treatment? claim)
       (no-humiliation? claim))))

(define degrading-treatment? (lambda (claim)
  (or (has-attribute claim 'humiliating-conduct)
      (has-attribute claim 'demeaning-conduct)
      (treats-as-object? claim))))

;; =============================================================================
;; SECTION 11 - LIFE DETAILED IMPLEMENTATIONS
;; =============================================================================

(define protection-of-life? (lambda (claim)
  (and (state-protects-life? claim)
       (no-arbitrary-deprivation? claim)
       (death-penalty-abolished? claim))))
;; =============================================================================
;; SECTION 12 - FREEDOM AND SECURITY OF PERSON DETAILED IMPLEMENTATIONS
;; =============================================================================

(define free-from-violence? (lambda (claim)
  (and (no-physical-violence? claim)
       (no-psychological-violence? claim)
       (no-domestic-violence? claim)
       (state-protection-from-violence? claim))))

(define free-from-torture? (lambda (claim)
  (and (no-torture? claim)
       (no-cruel-treatment? claim)
       (no-inhuman-treatment? claim)
       (no-degrading-punishment? claim))))

(define no-torture? (lambda (claim)
  (not (has-attribute claim 'torture))))

(define no-cruel-treatment? (lambda (claim)
  (not (has-attribute claim 'cruel-treatment))))

(define no-inhuman-treatment? (lambda (claim)
  (not (has-attribute claim 'inhuman-treatment))))

(define no-degrading-punishment? (lambda (claim)
  (not (has-attribute claim 'degrading-punishment))))

(define bodily-integrity? (lambda (claim)
  (and (control-over-body? claim)
       (security-in-person? claim)
       (no-medical-experimentation? claim)
       (no-forced-procedures? claim))))

(define control-over-body? (lambda (claim)
  (has-attribute claim 'bodily-autonomy)))

(define reproductive-freedom? (lambda (claim)
  (and (reproductive-choice? claim)
       (access-to-reproductive-healthcare? claim)
       (no-forced-sterilization? claim)
       (informed-consent-required? claim))))

;; =============================================================================
;; SECTION 13 - SLAVERY, SERVITUDE AND FORCED LABOUR IMPLEMENTATIONS
;; =============================================================================

(define not-enslaved? (lambda (claim)
  (and (not (has-attribute claim 'slavery))
       (free-status? claim)
       (not (owned-by-another? claim)))))

(define not-servitude? (lambda (claim)
  (and (not (has-attribute claim 'servitude))
       (not (bound-to-service? claim))
       (voluntary-service? claim))))

(define not-forced-labour? (lambda (claim)
  (and (not (has-attribute claim 'forced-labour))
       (voluntary-work? claim)
       (or (not (work-required? claim))
           (lawful-sentence-exception? claim)
           (emergency-exception? claim)))))
;; =============================================================================
;; SECTION 14 - PRIVACY DETAILED IMPLEMENTATIONS
;; =============================================================================

(define privacy-of-person? (lambda (claim)
  (and (personal-information-protected? claim)
       (identity-protected? claim)
       (no-unauthorized-surveillance? claim)
       (bodily-privacy? claim))))

(define privacy-of-home? (lambda (claim)
  (and (sanctity-of-home? claim)
       (no-unlawful-entry? claim)
       (no-unlawful-search? claim)
       (warrant-required-for-search? claim))))

(define privacy-of-property? (lambda (claim)
  (and (property-inviolable? claim)
       (no-unlawful-seizure? claim)
       (warrant-required-for-seizure? claim))))

(define privacy-of-communications? (lambda (claim)
  (and (confidential-communications? claim)
       (no-unlawful-interception? claim)
       (no-unauthorized-disclosure? claim)
       (encryption-permitted? claim))))

;; =============================================================================
;; SECTION 15 - FREEDOM OF RELIGION, BELIEF AND OPINION IMPLEMENTATIONS
;; =============================================================================

(define freedom-of-conscience? (lambda (claim)
  (and (conscience-protected? claim)
       (moral-convictions-protected? claim)
       (no-forced-conscience? claim))))

(define freedom-of-religion? (lambda (claim)
  (and (practice-religion? claim)
       (profess-religion? claim)
       (propagate-religion? claim)
       (religious-observance? claim)
       (no-established-religion? claim))))

(define practice-religion? (lambda (claim)
  (and (religious-acts-permitted? claim)
       (worship-permitted? claim)
       (reasonable-accommodation? claim))))

(define freedom-of-thought? (lambda (claim)
  (and (think-freely? claim)
       (hold-beliefs? claim)
       (change-beliefs? claim)
       (no-thought-control? claim))))

(define freedom-of-belief? (lambda (claim)
  (and (hold-beliefs-freely? claim)
       (religious-beliefs? claim)
       (non-religious-beliefs? claim)
       (no-coerced-belief? claim))))

(define freedom-of-opinion? (lambda (claim)
  (and (form-opinions? claim)
       (hold-opinions? claim)
       (express-opinions? claim)
       (no-penalty-for-opinion? claim))))

;; =============================================================================
;; SECTION 16 - FREEDOM OF EXPRESSION DETAILED IMPLEMENTATIONS
;; =============================================================================

(define freedom-of-press? (lambda (claim)
  (and (press-freedom? claim)
       (editorial-independence? claim)
       (no-censorship? claim)
       (investigative-journalism? claim))))

(define freedom-of-media? (lambda (claim)
  (and (media-independence? claim)
       (broadcast-freedom? claim)
       (publish-freely? claim)
       (diverse-media? claim))))

(define freedom-receive-information? (lambda (claim)
  (and (access-information? claim)
       (seek-information? claim)
       (obtain-information? claim)
       (no-information-blocking? claim))))

(define freedom-impart-information? (lambda (claim)
  (and (share-information? claim)
       (disseminate-information? claim)
       (communicate-ideas? claim)
       (no-prior-restraint? claim))))

(define artistic-creativity? (lambda (claim)
  (and (create-art? claim)
       (express-artistically? claim)
       (no-artistic-censorship? claim)
       (cultural-expression? claim))))

(define academic-freedom? (lambda (claim)
  (and (research-freedom? claim)
       (teach-freely? claim)
       (publish-findings? claim)
       (intellectual-independence? claim))))

(define scientific-research? (lambda (claim)
  (and (conduct-research? claim)
       (scientific-inquiry? claim)
       (no-research-censorship? claim)
       (ethical-research? claim))))
;; =============================================================================
;; SECTIONS 17-22 - ASSEMBLY, ASSOCIATION, POLITICAL AND MOVEMENT RIGHTS
;; =============================================================================

(define peaceful-assembly? (lambda (claim)
  (and (assembly-is-peaceful? claim)
       (no-violence-intended? claim)
       (lawful-purpose? claim)
       (orderly-assembly? claim))))

(define no-weapons-carried? (lambda (claim)
  (not (has-attribute claim 'weapons-present))))

(define freedom-to-associate? (lambda (claim)
  (and (join-association? claim)
       (form-association? claim)
       (leave-association? claim)
       (voluntary-association? claim))))

(define citizen? (lambda (person)
  (or (birth-citizen? person)
      (descent-citizen? person)
      (naturalized-citizen? person))))

(define birth-citizen? (lambda (person)
  (and (has-attribute person 'birth-in-sa)
       (born-after-1994? person))))

(define naturalized-citizen? (lambda (person)
  (and (has-attribute person 'naturalization-certificate)
       (meets-residency-requirements? person))))

(define right-to-vote? (lambda (person)
  (and (citizen? person)
       (age-18-or-older? person)
       (registered-voter? person)
       (not-disqualified? person))))

(define age-18-or-older? (lambda (person)
  (>= (get-attribute person 'age) 18)))

(define right-to-form-political-party? (lambda (person)
  (and (citizen? person)
       (freedom-of-association? person)
       (democratic-party? person))))

(define right-to-campaign? (lambda (person)
  (and (citizen? person)
       (freedom-of-expression? person)
       (peaceful-campaigning? person))))

(define free-to-move? (lambda (claim)
  (and (move-within-country? claim)
       (no-internal-restrictions? claim)
       (free-travel? claim))))

(define free-to-reside? (lambda (claim)
  (and (choose-residence? claim)
       (settle-anywhere? claim)
       (no-forced-relocation? claim))))

(define free-to-leave-country? (lambda (claim)
  (and (exit-permitted? claim)
       (passport-available? claim)
       (no-unlawful-restriction? claim))))

(define citizenship-not-deprived? (lambda (claim)
  (not (arbitrary-citizenship-loss? claim))))

(define freedom-of-occupation? (lambda (claim)
  (and (choose-trade? claim)
       (choose-occupation? claim)
       (choose-profession? claim)
       (reasonable-regulation-only? claim))))
;; =============================================================================
;; SECTIONS 23-32 - LABOUR, ENVIRONMENT, PROPERTY AND SOCIO-ECONOMIC RIGHTS
;; =============================================================================

(define right-to-fair-labour-practices? (lambda (worker)
  (and (fair-working-conditions? worker)
       (reasonable-working-hours? worker)
       (safe-workplace? worker)
       (fair-remuneration? worker))))

(define right-to-form-union? (lambda (worker)
  (and (freedom-of-association? worker)
       (organize-workers? worker)
       (establish-union? worker))))

(define right-to-join-union? (lambda (worker)
  (and (freedom-of-association? worker)
       (union-membership-voluntary? worker)
       (no-victimization? worker))))

(define right-to-strike? (lambda (worker)
  (and (protected-strike? worker)
       (advance-notice-given? worker)
       (peaceful-strike? worker)
       (lawful-purpose? worker))))

(define healthy-environment? (lambda (claim)
  (and (environment-not-harmful? claim)
       (clean-air? claim)
       (clean-water? claim)
       (pollution-controlled? claim))))

(define protected-environment? (lambda (claim)
  (and (conservation-measures? claim)
       (ecological-protection? claim)
       (biodiversity-protected? claim)
       (sustainable-use? claim))))

(define sustainable-development? (lambda (claim)
  (and (meets-present-needs? claim)
       (protects-future-generations? claim)
       (environmental-assessment? claim)
       (eco-friendly-development? claim))))

(define not-arbitrarily-deprived? (lambda (claim)
  (and (lawful-deprivation? claim)
       (due-process? claim)
       (fair-procedure? claim))))

(define expropriation-only-if-lawful? (lambda (claim)
  (and (public-purpose? claim)
       (public-interest? claim)
       (law-of-general-application? claim)
       (compensation-paid? claim))))

(define just-and-equitable-compensation? (lambda (claim)
  (and (market-value-considered? claim)
       (use-of-property-considered? claim)
       (history-of-acquisition-considered? claim)
       (purpose-of-expropriation-considered? claim)
       (balance-of-interests? claim))))

(define access-to-adequate-housing? (lambda (person)
  (and (housing-available? person)
       (affordable-housing? person)
       (habitable-housing? person)
       (accessible-housing? person))))

(define progressive-realisation? (lambda (person)
  (and (within-available-resources? person)
       (reasonable-measures-taken? person)
       (improving-over-time? person)
       (no-retrogressive-steps? person))))

(define access-to-healthcare? (lambda (person)
  (and (healthcare-services-available? person)
       (reproductive-healthcare? person)
       (emergency-treatment? person)
       (no-refusal-of-emergency-care? person))))

(define access-to-food? (lambda (person)
  (and (food-available? person)
       (sufficient-food? person)
       (nutritious-food? person)
       (food-security-programs? person))))

(define access-to-water? (lambda (person)
  (and (water-available? person)
       (sufficient-water? person)
       (safe-water? person)
       (affordable-water? person))))

(define social-security? (lambda (person)
  (and (social-assistance-available? person)
       (unable-to-support-self? person)
       (appropriate-social-grants? person))))
;; =============================================================================
;; SECTIONS 28-34 - CHILDREN, EDUCATION, CULTURE AND ACCESS RIGHTS
;; =============================================================================

(define child-best-interests-paramount? (lambda (child)
  (and (best-interests-primary? child)
       (child-welfare-priority? child)
       (all-decisions-consider-child? child))))

(define right-to-name? (lambda (child)
  (and (name-from-birth? child)
       (registered-name? child)
       (identity-through-name? child))))

(define right-to-nationality? (lambda (child)
  (and (citizenship-at-birth? child)
       (not-stateless? child)
       (nationality-documented? child))))

(define right-to-parental-care? (lambda (child)
  (and (parental-responsibility? child)
       (family-care? child)
       (alternative-care-if-needed? child)
       (maintain-family-ties? child))))

(define protection-from-abuse? (lambda (child)
  (and (no-maltreatment? child)
       (no-neglect? child)
       (no-degradation? child)
       (child-protection-services? child))))

(define basic-education? (lambda (person)
  (and (free-basic-education? person)
       (compulsory-education? person)
       (quality-education? person)
       (accessible-schools? person))))

(define further-education-reasonable-measures? (lambda (person)
  (and (progressive-access? person)
       (reasonable-steps-taken? person)
       (available-resources-used? person))))

(define use-language-of-choice? (lambda (person)
  (and (speak-own-language? person)
       (use-language-publicly? person)
       (use-language-privately? person)
       (no-language-discrimination? person))))

(define participate-in-cultural-life? (lambda (person)
  (and (engage-in-culture? person)
       (cultural-practices? person)
       (cultural-expression? person)
       (respect-for-culture? person))))

(define enjoy-culture? (lambda (community)
  (and (practice-culture? community)
       (preserve-culture? community)
       (develop-culture? community)
       (cultural-institutions? community))))

(define practice-religion? (lambda (community)
  (and (religious-observance? community)
       (religious-teaching? community)
       (religious-institutions? community)
       (freedom-from-coercion? community))))

(define use-language? (lambda (community)
  (and (speak-language? community)
       (teach-language? community)
       (develop-language? community)
       (language-institutions? community))))

(define access-to-information? (lambda (person)
  (and (request-information? person)
       (receive-information? person)
       (state-held-information? person)
       (timely-access? person)
       (reasonable-fee? person))))

(define lawful-action? (lambda (action)
  (and (authorized-by-law? action)
       (within-legal-powers? action)
       (proper-legal-basis? action))))

(define reasonable-action? (lambda (action)
  (and (rational-decision? action)
       (proportionate-action? action)
       (relevant-considerations? action)
       (no-irrelevant-considerations? action))))

(define procedurally-fair-action? (lambda (action)
  (and (adequate-notice? action)
       (opportunity-to-be-heard? action)
       (reasons-provided? action)
       (impartial-decision-maker? action))))

(define dispute-resolved-by-court? (lambda (dispute)
  (and (access-to-court? dispute)
       (jurisdiction-exists? dispute)
       (justiciable-dispute? dispute))))

(define fair-public-hearing? (lambda (dispute)
  (and (public-hearing? dispute)
       (fair-procedure? dispute)
       (impartial-tribunal? dispute)
       (reasonable-time? dispute))))
;; =============================================================================
;; SECTION 35 - ARRESTED, DETAINED AND ACCUSED PERSONS RIGHTS
;; =============================================================================

(define informed-of-rights? (lambda (person)
  (and (told-of-right-to-silence? person)
       (told-of-right-to-lawyer? person)
       (told-of-charges? person)
       (told-in-language-understood? person)
       (promptly-informed? person))))

(define right-to-remain-silent? (lambda (person)
  (and (silence-permitted? person)
       (no-compelled-confession? person)
       (no-self-incrimination? person)
       (no-adverse-inference? person))))

(define right-to-legal-representation? (lambda (person)
  (and (choose-lawyer? person)
       (consult-lawyer? person)
       (state-funded-if-indigent? person)
       (substantial-injustice-test? person))))

(define substantial-injustice-test? (lambda (person)
  (and (serious-offense? person)
       (unable-to-afford-lawyer? person)
       (complex-case? person))))

(define presumption-of-innocence? (lambda (person)
  (and (innocent-until-proven-guilty? person)
       (burden-on-prosecution? person)
       (beyond-reasonable-doubt? person))))

(define fair-trial? (lambda (person)
  (and (public-trial? person)
       (trial-without-delay? person)
       (present-at-trial? person)
       (understand-proceedings? person)
       (adduce-evidence? person)
       (challenge-evidence? person)
       (cross-examine-witnesses? person)
       (appeal-conviction? person))))

;; =============================================================================
;; SECTION 36 - LIMITATION OF RIGHTS DETAILED IMPLEMENTATIONS
;; =============================================================================

(define law-of-general-application? (lambda (limitation)
  (and (applies-generally? limitation)
       (not-arbitrary? limitation)
       (clear-and-accessible? limitation)
       (prospective-application? limitation))))

(define reasonable-limitation? (lambda (limitation)
  (and (rational-basis? limitation)
       (proportionate? limitation)
       (necessary? limitation)
       (achieves-purpose? limitation))))

(define justifiable-in-open-democratic-society? (lambda (limitation)
  (and (democratic-values? limitation)
       (human-rights-culture? limitation)
       (open-society? limitation)
       (accountable-government? limitation))))

(define passes-proportionality-test? (lambda (limitation right)
  (and (suitability? limitation)
       (necessity? limitation)
       (proportionality-stricto-sensu? limitation right))))

(define suitability? (lambda (limitation)
  (and (achieves-objective? limitation)
       (rationally-connected? limitation))))

(define necessity? (lambda (limitation)
  (and (no-less-restrictive-means? limitation)
       (minimally-impairing? limitation))))

(define proportionality-stricto-sensu? (lambda (limitation right)
  (and (benefits-outweigh-costs? limitation right)
       (not-excessive? limitation)
       (balanced-approach? limitation right))))

(define consider-nature-of-right? (lambda (limitation right)
  (and (importance-of-right? right)
       (centrality-to-dignity? right)
       (role-in-democracy? right))))

(define consider-importance-of-purpose? (lambda (limitation)
  (and (legitimate-purpose? limitation)
       (pressing-need? limitation)
       (substantial-objective? limitation))))

(define consider-nature-and-extent? (lambda (limitation)
  (and (scope-of-limitation? limitation)
       (duration-of-limitation? limitation)
       (severity-of-impact? limitation))))

(define consider-less-restrictive-means? (lambda (limitation)
  (and (alternatives-considered? limitation)
       (minimal-impairment? limitation)
       (least-drastic-means? limitation))))

(define balance-achieved? (lambda (limitation right)
  (and (weighing-completed? limitation right)
       (proportionate-result? limitation right)
       (reasonable-balance? limitation right))))
;; =============================================================================
;; SEPARATION OF POWERS AND GOVERNMENT STRUCTURE
;; =============================================================================

(define national-parliament? (lambda (body)
  (and (has-attribute body 'legislative-authority)
       (national-assembly? body)
       (national-council-provinces? body))))

(define provincial-legislature? (lambda (body)
  (and (has-attribute body 'provincial-legislative-power)
       (elected-members? body)
       (provincial-jurisdiction? body))))

(define president? (lambda (body)
  (and (head-of-state? body)
       (head-of-executive? body)
       (elected-by-parliament? body))))

(define cabinet? (lambda (body)
  (and (executive-authority? body)
       (president-and-ministers? body)
       (collective-decision-making? body))))

(define deputy-ministers? (lambda (body)
  (and (assist-ministers? body)
       (executive-function? body)
       (appointed-by-president? body))))

(define provincial-executive? (lambda (body)
  (and (provincial-authority? body)
       (premier-and-mecs? body)
       (provincial-governance? body))))

(define independent-court? (lambda (body)
  (and (judicial-authority? body)
       (free-from-interference? body)
       (institutional-independence? body)
       (decisional-independence? body))))

(define impartial-court? (lambda (body)
  (and (no-bias? body)
       (fair-adjudication? body)
       (objective-decision-making? body))))

(define subject-only-to-constitution? (lambda (body)
  (and (constitutional-supremacy? body)
       (no-political-direction? body)
       (law-alone-governs? body))))

;; =============================================================================
;; COOPERATIVE GOVERNMENT (CHAPTER 3)
;; =============================================================================

(define national-sphere? (lambda (sphere)
  (and (has-attribute sphere 'national-government)
       (national-competence? sphere)
       (national-jurisdiction? sphere))))

(define provincial-sphere? (lambda (sphere)
  (and (has-attribute sphere 'provincial-government)
       (provincial-competence? sphere)
       (provincial-boundaries? sphere))))

(define local-sphere? (lambda (sphere)
  (and (has-attribute sphere 'local-government)
       (municipal-jurisdiction? sphere)
       (local-service-delivery? sphere))))

(define distinctive-interdependent? (lambda (sphere)
  (and (separate-sphere? sphere)
       (depends-on-others? sphere)
       (coordinate-activities? sphere))))

(define interrelated-sphere? (lambda (sphere)
  (and (connected-spheres? sphere)
       (cooperative-relations? sphere)
       (mutual-support? sphere))))

;; =============================================================================
;; CONSTITUTIONAL COURT JURISDICTION
;; =============================================================================

(define constitutional-matter? (lambda (matter)
  (or (interpretation-of-constitution? matter)
      (protection-of-constitution? matter)
      (enforcement-of-constitution? matter)
      (validity-of-law? matter)
      (constitutional-amendment-dispute? matter))))

(define matter-connected-with-constitutional? (lambda (matter)
  (and (constitutional-question-arises? matter)
       (constitutional-issue-material? matter)
       (constitutional-interpretation-needed? matter))))

(define exclusive-jurisdiction-matter? (lambda (matter)
  (or (disputes-between-organs-state? matter)
      (constitutionality-amendment? matter)
      (election-disputes? matter)
      (constitutional-validity-parliament-act? matter))))

(define interpretation-of-constitution? (lambda (matter)
  (and (constitutional-provision-disputed? matter)
       (meaning-unclear? matter)
       (authoritative-interpretation-needed? matter))))

(define protection-of-constitution? (lambda (matter)
  (and (constitutional-violation? matter)
       (constitutional-supremacy-threatened? matter)
       (court-intervention-needed? matter))))

(define enforcement-of-constitution? (lambda (matter)
  (and (constitutional-right-infringed? matter)
       (remedy-required? matter)
       (constitutional-order-needed? matter))))

;; =============================================================================
;; HELPER FUNCTIONS AND UTILITIES
;; =============================================================================

(define has-attribute (lambda (entity attribute)
  (and (not (null? entity))
       (if (pair? entity)
           (or (eq? (car entity) attribute)
               (has-attribute (cdr entity) attribute))
           (eq? entity attribute)))))

(define get-attribute (lambda (entity attribute)
  (if (has-attribute entity attribute)
      attribute
      #f)))

(define human-being? (lambda (entity)
  (has-attribute entity 'natural-person)))

(define company? (lambda (entity)
  (has-attribute entity 'company)))

(define close-corporation? (lambda (entity)
  (has-attribute entity 'cc)))

(define trust? (lambda (entity)
  (has-attribute entity 'trust)))

(define non-profit-organization? (lambda (entity)
  (has-attribute entity 'npo)))

(define born-after-1994? (lambda (person)
  (> (get-attribute person 'birth-year) 1994)))

(define registered-voter? (lambda (person)
  (has-attribute person 'voter-registration)))

(define not-disqualified? (lambda (person)
  (not (has-attribute person 'voting-disqualification))))

(define meets-residency-requirements? (lambda (person)
  (>= (get-attribute person 'years-resident) 5)))

(define democratic-party? (lambda (person)
  (has-attribute person 'democratic-principles)))

(define peaceful-campaigning? (lambda (person)
  (not (has-attribute person 'violent-campaigning))))

(define reasonable-regulation-only? (lambda (claim)
  (and (regulation-exists? claim)
       (proportionate-regulation? claim))))

(define lawful-purpose? (lambda (claim)
  (not (has-attribute claim 'unlawful-purpose))))

(define orderly-assembly? (lambda (claim)
  (has-attribute claim 'orderly)))

(define voluntary-association? (lambda (claim)
  (not (has-attribute claim 'forced-membership))))

(define serious-offense? (lambda (person)
  (or (has-attribute person 'schedule-5-offense)
      (has-attribute person 'schedule-6-offense))))

(define unable-to-afford-lawyer? (lambda (person)
  (has-attribute person 'indigent)))

(define complex-case? (lambda (person)
  (has-attribute person 'complex-legal-issues)))

(define innocent-until-proven-guilty? (lambda (person)
  (not (has-attribute person 'guilt-presumed))))

(define beyond-reasonable-doubt? (lambda (person)
  (has-attribute person 'high-standard-proof)))

(define applies-generally? (lambda (limitation)
  (not (has-attribute limitation 'specific-target))))

(define not-arbitrary? (lambda (limitation)
  (has-attribute limitation 'rational-basis)))

(define clear-and-accessible? (lambda (limitation)
  (and (has-attribute limitation 'clear-language)
       (has-attribute limitation 'publicly-available))))

(define prospective-application? (lambda (limitation)
  (not (has-attribute limitation 'retrospective))))

(define rational-basis? (lambda (limitation)
  (has-attribute limitation 'rational-connection)))

(define proportionate? (lambda (limitation)
  (has-attribute limitation 'proportionate-means)))

(define necessary? (lambda (limitation)
  (has-attribute limitation 'necessary-measure)))

(define achieves-purpose? (lambda (limitation)
  (has-attribute limitation 'effective)))

(define democratic-values? (lambda (limitation)
  (has-attribute limitation 'democratic-society)))

(define human-rights-culture? (lambda (limitation)
  (has-attribute limitation 'respects-rights)))

(define open-society? (lambda (limitation)
  (not (has-attribute limitation 'authoritarian)))

(define accountable-government? (lambda (limitation)
  (has-attribute limitation 'accountable)))

(define achieves-objective? (lambda (limitation)
  (has-attribute limitation 'objective-achieved)))

(define rationally-connected? (lambda (limitation)
  (has-attribute limitation 'rational-link)))

(define no-less-restrictive-means? (lambda (limitation)
  (not (has-attribute limitation 'alternative-available))))

(define minimally-impairing? (lambda (limitation)
  (has-attribute limitation 'minimal-impairment)))

(define benefits-outweigh-costs? (lambda (limitation right)
  (> (get-attribute limitation 'benefit-score) 
     (get-attribute right 'cost-score))))

(define not-excessive? (lambda (limitation)
  (not (has-attribute limitation 'excessive))))

(define balanced-approach? (lambda (limitation right)
  (has-attribute limitation 'balanced)))

(define importance-of-right? (lambda (right)
  (has-attribute right 'important)))

(define centrality-to-dignity? (lambda (right)
  (has-attribute right 'dignity-related)))

(define role-in-democracy? (lambda (right)
  (has-attribute right 'democratic-essential)))

(define legitimate-purpose? (lambda (limitation)
  (has-attribute limitation 'legitimate-aim)))

(define pressing-need? (lambda (limitation)
  (has-attribute limitation 'urgent)))

(define substantial-objective? (lambda (limitation)
  (has-attribute limitation 'substantial-goal)))

(define scope-of-limitation? (lambda (limitation)
  (get-attribute limitation 'scope)))

(define duration-of-limitation? (lambda (limitation)
  (get-attribute limitation 'duration)))

(define severity-of-impact? (lambda (limitation)
  (get-attribute limitation 'severity)))

(define alternatives-considered? (lambda (limitation)
  (has-attribute limitation 'alternatives-examined)))

(define minimal-impairment? (lambda (limitation)
  (has-attribute limitation 'least-restrictive)))

(define least-drastic-means? (lambda (limitation)
  (has-attribute limitation 'minimal-restriction)))

(define weighing-completed? (lambda (limitation right)
  (has-attribute limitation 'balanced-analysis)))

(define proportionate-result? (lambda (limitation right)
  (has-attribute limitation 'proportionate-outcome)))

(define reasonable-balance? (lambda (limitation right)
  (has-attribute limitation 'reasonable-equilibrium)))

;; =============================================================================
;; END OF SOUTH AFRICAN CONSTITUTIONAL LAW FRAMEWORK
;; =============================================================================

;; This framework provides the foundational structure for implementing
;; South African constitutional law in a rule-based system.

// location: frontend/src/components

// SettingsModal({ isOpen })

// LandingPage/Main({})
// LandingPage/Header({})
// LandingPage/Footer({})
// LandingPage/NeuronImage({ size="size-24", classes="" })
// LandingPage/FeatureList({ headline, title, description, features })
// LandingPage/LifetimePrice({ price="$40" })
// LandingPage/PricingSection1({})
// LandingPage/PricingSection2({ headline, description, paymentOptions, selectedPriceOption, freePlanAddition=false, options })
// LandingPage/TestimonialCards({})

// HomePage/Main({})

// Subscription/Subscription({})
// Subscription/Details({ keyClass, valueClass, planName="Free", planAccess, autoUpdateWidth })
// Subscription/RecursiveJSON({ data, autoUpdateWidth=false, keyFormattingFunction, valueFormattingFunction, valueClass, keyClass, nestLevel=0 })
// Subscription/PaymentOptionModal({ price="$5.00", open=false, selectedPlanType, currentPlanType, options })
// Subscription/StripePaymentModal({ open=false, subscriptionId, clientSecret })

// organizer/ActiveTimer({ session, task })          — live elapsed timer with Stop button; dispatches 'stop'
// organizer/TaskCard({ task, activeSessionTaskId, sections }) — urgency badge, meta, Start/Stop; dispatches 'start','stop','edit','delete'
// organizer/TaskModal({ open, task, sections })     — create/edit task form; dispatches 'save','close'
// organizer/ScheduleGrid({ schedule })              — 7-column week view with urgency-colored task pills
// organizer/SectionsSidebar({ sections, selectedId }) — sidebar for section management; dispatches 'select'(id|null),'add'({name,day_configs}),'editRequest'(section),'delete'
// organizer/SectionEditModal({ open, section })     — per-day schedule editor (time_block/duration/off per day, copy-to-all); dispatches 'save','close'
// organizer/StatsPanel({ stats, sections })         — dashboard with SVG donut chart by section + sortable task table with section tabs

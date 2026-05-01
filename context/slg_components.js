// location: frontend/src/components/slg

// primitives
// Button({ example, disabled, componentType="basic", loaderStyle, loading, loaderSize, buttonType="button", size="md", classes })
// Link({ example, href="#" })
// Code({ example, bg, componentType="Linux" })

// modals
// Modal({ open=false, center=false, modalPosition="body" })
// BaseModal({ example, cssPosition="fixed", position="top-center", open=false, canOpen=true, onClose, openDelay=0 })

// confirmation
// Confirm({ example, open=false, canOpen=true, position="middle-center", confirmButtonClass, cancelButtonClass, confirmCallback })
// Delete({ example, open=false, canOpen=true, position="middle-center", deleteCallback })
// DeleteWithInput({ example, open=false, canOpen=true, position="middle-center", inputRequired, input="", deleteCallback })

// informative
// Tooltip({ tooltipPos="top", debounceTime=250, hideDelay=150, _hideTimeout, showTooltip=false, example })
// Info({ example, size="h-4 w-4", tooltipPos="top", hideDelay=150, _hideTimeout, showTooltip })
// Toast({})

// forms/inputs
// Simple({ componentType="standard", id, label, description, value, placeholder, hint, inputClasses, labelClasses, disabled, addonText, icon, trailingIcon })
// WithSlider({ id, label, labelClasses, inputClasses, min=0, max=2, step=0.01, value, disabled, placeholder })
// PasswordWithVisToggle({ password })

// forms/selects
// Simple({ label, options, open=false, labelClasses, buttonClasses, dropdownClasses, disabled, value })

// forms/checkboxes
// Checkbox({ componentType="inline", checked=false, title, description, id })
// CheckboxGroup({ componentType="inline", checkboxes })

// forms/sliders
// Slider({ min=1, max=100, value=50 })
// Slider2({ min=0, max=2, step=0.01, value })
// RangeSlider({ min=1, max=100, value=50, darkColorWeight=400, colorWeight=600 })

// forms/combinations
// CheckboxInput({ id, label, description, placeholder, checked=false, value, inputClasses })
// CheckboxSelect({ label, description, checked=false, options, value, buttonClasses, dropdownClasses })
// SelectInputCombo({ options, label, value, selectValue, selectedIndex=0 })

// forms/category
// DefineCategory({ defaultRule, defaultCategory, addNewDefinitionsWhere="back", storageKey, category, removingHoverTime=25 })
// DefineCategoryGroup({ title, confirmDelete=true, confirmDeletePosition, tooltipPos, tooltip, whereToAddNewCategoryGroups, defaultRule, defaultCategory, categoryDefinitions })

// navs
// NavTop({ navObjects, brandName, brandImage, brandSize, brandTLD, header, searchBar=false })
// NavLeft({ items=[], bottomItems=[], fontSize, textColor, closedWidth, openWidth })
// NavLeft2({ accordionTabs, fontSize, textColor, width, baseColor, baseStrength })
// NestedTreeNavLeft({ treeObject, width, baseColor, baseStrength })
// NestedTreeNavLeft2({ treeObject, width, baseColor, baseStrength })
// NestedTreeNavLeftWrapper({ treeObject })
// NavListOne({ items=[] })

// navs/hero
// Top({ example, logo, includeLogo=true, includeDarkToggle=true, navObjects, rightSide="contact", rightSideHref })

// layouts
// FullWidthNarrowSidebar({ breakpoint="lg", includeProfile=true, logo, navObjects })
// TwoColumnLayout({ breakpoint="lg" })
// NavTopWithOverlap({ navObjects, brandName, brandImage, brandSize, header })
// SidebarNavSearchHeader({})

// accordions
// NestedAccordion({ folderName, treeObject, depth=0, textColorOne, textColorTwo })
// NestedAccordion2({ folderName, treeObject, depth=0, accordionButtonColor, contentColor, open=false })

// tabs
// TabsUnderline({ tabNames, tabContent, useBuiltinContent=true, selectedIdx=0, breakpoint="md", example, activeTab })
// TabContent({ example, startIdx=0, variableIdx=0 })
// TabsEditableUnderline({ tabNames, selectedIdx=0, inputValue, breakpoint="md", includeDelete=true, deleteText })

// pagination
// ListPagination({ example, elements, elementsPerPage=4, numPages, currentPage=1 })
// NumberButtonGroup({ pageNums, active=0, example, activeBackground })

// lists
// IconList({ example, height, bgColor, ringColor, ringSize, baseDir, includeTooltip=true, icons })
// FeatureList({ example, features })
// SocialLinks({ example, size, color, ringColor, ringSize, baseDir, includeTooltip=true, links })

// dropdowns
// DropdownOne({})

// cards
// OneLineCard({})

// loaders
// Loader({ size="size-6" })
// Liquid({})
// Liquid2({ animStartTime=0 })
// Liquid3({ animStartTime=0 })
// LiquidFillContainer({})

// toggles
// LightDark({ condensed=false, moonColorStrength1=600, moonColorStrength2=400, borderColor })

// wrappers
// AnimateOnScroll({ animation, offset, delay, duration, easing, mirror, once, anchorPlacement, example })

// backdrops
// DocumentBackdrop({ visible=false, fadeDuration=500 })
// BodyBackdrop({})

// media/video
// VideoPlayer({ example })
// VideoModal({ example, buttonText, source, poster, width, modal, open, btnClass })
// TapSidesToSeek({})
// Vime({ source, poster })

// media/audio
// SoundTest({ soundPath, vol=0.4 })

// datatable
// SvelTable({ example, dataSet, numRows=30 })
// Heading({ displayText, arrow, colID=0, isSortedAtoZ })
// Cell({ displayText, colID=0, rowID=0 })
// CellRow({ rowData })
// VirtualList({ items, height="100%", itemHeight, start=0, end=0 })

// tables
// Checkboxes({ title, description, example, rowClickCallback, headers, rows, selectedRows })

// charts
// Frappe({ data, title, type="line", height=300, animate=true, axisOptions, barOptions, lineOptions, tooltipOptions, colors, valuesOverPoints, isNavigable, maxSlices })

// links
// LinkNewTab({ example, href="#", text="Visit", direction="right" })

// images
// TrendingUpArrow({ classes })
// TrendingDownArrow({ classes })

// scroll/buttons
// ScrollDown({ href="#", name, shouldScroll=true, scrollDuration=1500 })

// scrollers
// HorizontalScrollingDiv({})

// iframe
// IFrame({ width=100 })

// time
// TimeRange({ format, range, color })

// files
// JSONReader({ example, jsonData })
// CsvReader({ optClass, numCols, columnHeaders, csvData, fileUploaded })
// UploadAnimation({})

// user
// AccountNavItems({})

// hero
// HeroOne({ logo, headerText1, headerText2, descriptionText, button1, button2, scrollDuration, navObjects, includeLogo, includeDarkToggle, rightSide, rightSideHref })

// tailwind/landing-pages
// IllustratedHero({ configLocation, navigationObjects, brandSvg, brandPng, header1, header2, description, img, navRightObjects })

// tailwind/FeatureSections
// Offset2x2Grid({ example, bg, img })

// tailwind/Contact
// Basic({ example, serverEndpoint, title, descriptionText, displayEmail, displayPhoneNumber, street, cityStateZip })

// portfolio/highlights
// Project({ offset, animationParamsLeft, animationParamsRight, imgSrc, imgAlt, examples, id, transition, descriptionSide, hideUntilVisible })
// ProjectLeft({ id, offset, animationParamsLeft, animationParamsRight })
// ProjectRight({ id, transition, side, hideUntilVisible })

// portfolio/experience
// JobVertical({ example, bgColor, company, job, role, valueAdded, dateRange, img, imgBgColor })

// handdrawn
// DescriptionWithArrowRight({ size="size-24" })
// DescriptionWithArrowUp({ size="size-24" })
// DescriptionWithArrowTRtoBL({})

// RadioMultiSelect({ choices, disabledChoices, disabledInfo, activeChoice, wrapperClass, textSize, squareEdges, color, baseClass, inactiveClass, activeClass })
// Loader({ classes="" })
// Portal({})

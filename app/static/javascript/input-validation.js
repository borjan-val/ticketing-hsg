function ticket_input_validate(ticket_input_element) {
	ticket_input_element.value =
		ticket_input_element.value
		.toUpperCase()
		.replace(/[^A-Z0-9]/g, '')
		.slice(0, 6)
}
function username_validate(text_input_element) {
	text_input_element.value =
		text_input_element.value
		.replace(/[^A-Za-z0-9\.\-\+_@#]/g, '')
}
function grade_validate(number_input_element) {
	number_input_element.value =
		number_input_element
		.replace(/[^0-9]/g, '')
		.slice(0, 2)
}
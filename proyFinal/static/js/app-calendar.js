'use strict';

var direction = 'ltr';  // o 'rtl' según tu lógica

if (isRtl) {
  direction = 'rtl';
}

document.addEventListener('DOMContentLoaded', function () {
  
  (function () {
    const calendarEl = document.getElementById('calendar'),
      appCalendarSidebar = document.querySelector('.app-calendar-sidebar'),
      addEventSidebar = document.getElementById('addEventSidebar'),
      appOverlay = document.querySelector('.app-overlay'),
       tipoEventoColor = {
            1: 'primary',
            2: 'success',
            3: 'danger',
            4: 'warning',
            5: 'info',
            6: 'recaudacion',
          },
      offcanvasTitle = document.querySelector('.offcanvas-title'),
      btnToggleSidebar = document.querySelector('.btn-toggle-sidebar'),
      btnSubmit = document.querySelector('#addEventBtn'),
      btnDeleteEvent = document.querySelector('.btn-delete-event'),
      btnCancel = document.querySelector('.btn-cancel'),
      eventTitle = document.querySelector('#titulo'),
      tipoEvento = document.querySelector('#tipoEvento'),
      categoria = document.querySelector('#categoria'),
      localidad = document.querySelector('#localidad'),
      eventStartDate = document.querySelector('#eventStartDate'),
      eventEndDate = document.querySelector('#eventEndDate'),
          
      contrincante = document.querySelector('#contrincante-wrapper'),
      rama = document.querySelector('#rama'),
      division = document.querySelector('#division'),

      eventLocation = document.querySelector('#eventLocation'),
      eventDescription = document.querySelector('#descripcion'),
      allDaySwitch = document.querySelector('#todoElDia'),
      selectAll = document.querySelector('.select-all'),
      filterInput = [].slice.call(document.querySelectorAll('.input-filter')),
      inlineCalendar = document.querySelector('.inline-calendar');

    let eventToUpdate,
      //currentEvents = events, // Assign app-calendar-events.js file events (assume events from API) to currentEvents (browser store/object) to manage and update calender events
      isFormValid = false,
      inlineCalInstance;

    // Init event Offcanvas
    const bsAddEventSidebar = new bootstrap.Offcanvas(addEventSidebar);

    // Event start (flatpicker)
    if (eventStartDate) {
      var start = eventStartDate.flatpickr({
        locale: flatpickr.l10ns.es,
        enableTime: true,
        altFormat: 'Y-m-dTH:i:S',
        onReady: function (selectedDates, dateStr, instance) {
          if (instance.isMobile) {
            instance.mobileInput.setAttribute('step', null);
          }
        }
      });
    }

    // Event end (flatpicker)
    if (eventEndDate) {
      var end = eventEndDate.flatpickr({
        locale: flatpickr.l10ns.es,
        enableTime: true,
        altFormat: 'Y-m-dTH:i:S',
        onReady: function (selectedDates, dateStr, instance) {
          if (instance.isMobile) {
            instance.mobileInput.setAttribute('step', null);
          }
        }
      });
    }

    // Inline sidebar calendar (flatpicker)
    if (inlineCalendar) {
      inlineCalInstance = inlineCalendar.flatpickr({
        locale: flatpickr.l10ns.es,
        monthSelectorType: 'static',
        inline: true
      });
    }

function mostrarCamposSegunTipo() {
  const tipo = tipoEvento.value;
console.log("tipoEvento:", tipoEvento);

  // Definimos los wrappers directos por id
  const wrappers = {
    titulo: document.getElementById('titulo-wrapper'),
    tipoEvento: document.getElementById('tipoEvento-wrapper'),
    categoria: document.getElementById('categoria-wrapper'),
    localidad: document.getElementById('localidad-wrapper'),
    contrincante: document.getElementById('contrincante-wrapper'),
    rama: document.getElementById('rama-wrapper'),
    division: document.getElementById('division-wrapper'),
    descripcion: document.getElementById('descripcion-wrapper'),
    todoElDia: document.getElementById('todoElDia-wrapper'),
    eventStartDate: document.getElementById('fechaInicio-wrapper'),
    eventEndDate: document.getElementById('fechaFin-wrapper')
  };

  // Ocultar todos
  Object.values(wrappers).forEach(w => { if (w) w.style.display = 'none'; });

  if (wrappers.tipoEvento) wrappers.tipoEvento.style.display = 'block';

  // Mostrar según tipo
  switch (tipo) {
    case '1': // Entrenamiento
      [wrappers.tipoEvento, wrappers.titulo, wrappers.eventStartDate]
        .forEach(w => w && (w.style.display = 'block'));
      break;

    case '2': // Partido
      [wrappers.tipoEvento, wrappers.titulowrappers.eventStartDate,
       wrappers.localidad, wrappers.contrincante, wrappers.rama, wrappers.division]
        .forEach(w => w && (w.style.display = 'block'));
      break;

    case '3': // Vacaciones
      [wrappers.tipoEvento, wrappers.titulo,
       wrappers.eventStartDate, wrappers.eventEndDate]
        .forEach(w => w && (w.style.display = 'block'));
      break;

    case '4':
    case '5':
    case '6': // Suspensión, Torneo, Recaudación
      [wrappers.tipoEvento, wrappers.titulo, wrappers.eventStartDate,
       wrappers.categoria, wrappers.localidad, wrappers.descripcion]
        .forEach(w => w && (w.style.display = 'block'));
      break;
    default:
    if (wrappers.tipoEvento) wrappers.tipoEvento.style.display = 'block';
    break;
  }
}

    // Event listener
    if (tipoEvento) {
      // Escucha cambios de Select2
      $(tipoEvento).on('change', mostrarCamposSegunTipo);

      // Llamada inicial
      mostrarCamposSegunTipo();
    }

    // Event click function
    function eventClick(info) {
      eventToUpdate = info.event;
      if (eventToUpdate.url) {
        info.jsEvent.preventDefault();
        window.open(eventToUpdate.url, '_blank');
      }
      bsAddEventSidebar.show();
      // For update event set offcanvas title text: Update Event
      if (offcanvasTitle) {
        offcanvasTitle.innerHTML = 'Actualizar Evento';
      }
      btnSubmit.innerHTML = 'Actualizar';
      btnSubmit.classList.add('btn-update-event');
      btnSubmit.classList.remove('btn-add-event');
      btnDeleteEvent.classList.remove('d-none');

      eventTitle.value = eventToUpdate.title;
      localidad.value  =eventToUpdate.localidad;
      categoria.value = eventToUpdate.categoria;
      tipoEvento.value = eventToUpdate.extendedProps.tipoEvento;
      start.setDate(eventToUpdate.start, true, 'Y-m-d');
      eventToUpdate.allDay === true ? (allDaySwitch.checked = true) : (allDaySwitch.checked = false);
      eventToUpdate.end !== null
        ? end.setDate(eventToUpdate.end, true, 'Y-m-d')
        : end.setDate(eventToUpdate.start, true, 'Y-m-d');
      eventToUpdate.extendedProps.description !== undefined
        ? (eventDescription.value = eventToUpdate.extendedProps.description)
        : null;

      // // Call removeEvent function
      // btnDeleteEvent.addEventListener('click', e => {
      //   removeEvent(parseInt(eventToUpdate.id));
      //   // eventToUpdate.remove();
      //   bsAddEventSidebar.hide();
      // });
    }

    // Modify sidebar toggler
    function modifyToggler() {
      const fcSidebarToggleButton = document.querySelector('.fc-sidebarToggle-button');
      const fcPrevButton = document.querySelector('.fc-prev-button');
      const fcNextButton = document.querySelector('.fc-next-button');
      const fcHeaderToolbar = document.querySelector('.fc-header-toolbar');
      fcPrevButton.classList.add('btn', 'btn-sm', 'btn-icon', 'btn-outline-secondary', 'me-2');
      fcNextButton.classList.add('btn', 'btn-sm', 'btn-icon', 'btn-outline-secondary', 'me-4');
      fcHeaderToolbar.classList.add('row-gap-4', 'gap-2');
      fcSidebarToggleButton.classList.remove('fc-button-primary');
      fcSidebarToggleButton.classList.add('d-lg-none', 'd-inline-block', 'ps-0');
      while (fcSidebarToggleButton.firstChild) {
        fcSidebarToggleButton.firstChild.remove();
      }
      fcSidebarToggleButton.setAttribute('data-bs-toggle', 'sidebar');
      fcSidebarToggleButton.setAttribute('data-overlay', '');
      fcSidebarToggleButton.setAttribute('data-target', '#app-calendar-sidebar');
      fcSidebarToggleButton.insertAdjacentHTML('beforeend', '<i class="ri-menu-line ri-24px text-body"></i>');
    }

    // Filter events by calender
    function selectedCalendars() {
      let selected = [],
        filterInputChecked = [].slice.call(document.querySelectorAll('.input-filter:checked'));

      filterInputChecked.forEach(item => {
        selected.push(item.getAttribute('data-value'));
      });

      return selected;
    }

    // --------------------------------------------------------------------------------------------------
    // AXIOS: fetchEvents
    // * This will be called by fullCalendar to fetch events. Also this can be used to refetch events.
    // --------------------------------------------------------------------------------------------------
    function fetchEvents(info, successCallback) {
      // Fetch Events from API endpoint reference
      /* $.ajax(
        {
          url: '../../../app-assets/data/app-calendar-events.js',
          type: 'GET',
          success: function (result) {
            // Get requested calendars as Array
            var calendars = selectedCalendars();

            return [result.events.filter(event => calendars.includes(event.extendedProps.calendar))];
          },
          error: function (error) {
            console.log(error);
          }
        }
      ); */

      let calendars = selectedCalendars();
      // We are reading event object from app-calendar-events.js file directly by including that file above app-calendar file.
      // You should make an API call, look into above commented API call for reference
      let selectedEvents = currentEvents.filter(function (event) {
        
        // console.log(event.extendedProps.calendar.toLowerCase());
        return calendars.includes(event.extendedProps.calendar.toLowerCase());
      });
      // if (selectedEvents.length > 0) {
      successCallback(selectedEvents);
      // }
    }

    // Init FullCalendar
    // ------------------------------------------------
    let calendar = new Calendar(calendarEl, {
      locale: 'es',
      initialView: 'dayGridMonth',
       displayEventTime: false,
       buttonText: {
        dayGridMonth: 'Mes',
        timeGridWeek: 'Semana',
        timeGridDay: 'Día',
        listMonth: 'Lista'
      },
       events: {
          url: '/eventos',
          method: 'GET',
          extraParams: function() {
            const checkedBoxes = document.querySelectorAll('input[name="tipoEventos[]"]:checked');
            const params = {};
            params['tipoEventos[]'] = [];
            checkedBoxes.forEach(cb => {
              params['tipoEventos[]'].push(cb.value);
            });
            return params;
          }
        },
      plugins: [dayGridPlugin, interactionPlugin, listPlugin, timegridPlugin],
      editable: true,
      dragScroll: true,
      dayMaxEvents: 2,
      eventResizableFromStart: true,
      customButtons: {
        sidebarToggle: {
          text: 'Sidebar'
        }
      },
      headerToolbar: {
        locale: 'es',
        start: 'sidebarToggle, prev,next, title',
        end: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'
      },
      direction: direction,
      initialDate: new Date(),
      navLinks: true, // can click day/week names to navigate views
      eventClassNames: function ({ event: calendarEvent }) {
        const tipo = calendarEvent.extendedProps.calendar; // ← ahora es un número
        const colorClass = tipoEventoColor[tipo];
        return colorClass ? ['fc-event-' + colorClass] : [];
      },
      dateClick: function (info) {
        let date = moment(info.date).format('YYYY-MM-DD');
        resetValues();
        bsAddEventSidebar.show();

        // For new event set offcanvas title text: Add Event
        if (offcanvasTitle) {
          offcanvasTitle.innerHTML = 'Agregar Evento';
        }
        btnSubmit.innerHTML = 'Agregar';
        btnSubmit.classList.remove('btn-update-event');
        btnSubmit.classList.add('btn-add-event');
        btnDeleteEvent.classList.add('d-none');
        eventStartDate.value = date;
        eventEndDate.value = date;
      },
      eventClick: function (info) {
        eventClick(info);
      },
      datesSet: function () {
        modifyToggler();
      },
      viewDidMount: function () {
        modifyToggler();
      }
    });

    // Render calendar
    calendar.render();
    // Modify sidebar toggler
    modifyToggler();

    const eventForm = document.getElementById('eventForm');
    const fv = FormValidation.formValidation(eventForm, {
      fields: {
        eventTitle: {
          validators: {
            notEmpty: {
              message: 'Por favor complete el Titulo'
            }
          }
        },
        eventStartDate: {
          validators: {
            notEmpty: {
              message: 'Por favor complete la fecha de inicio '
            }
          }
        },
        eventEndDate: {
          validators: {
            notEmpty: {
              message: 'Por favor complete la fecha de fin '
            }
          }
        }
      },
      plugins: {
        trigger: new FormValidation.plugins.Trigger(),
        bootstrap5: new FormValidation.plugins.Bootstrap5({
          eleValidClass: '',
          rowSelector: function (field, ele) {
            return '.mb-5';
          }
        }),
        submitButton: new FormValidation.plugins.SubmitButton(),
        defaultSubmit: new FormValidation.plugins.DefaultSubmit(), // ✅ Esto envía el form
        autoFocus: new FormValidation.plugins.AutoFocus()
      }
    })
      .on('core.form.valid', function () {
        // Jump to the next step when all fields in the current step are valid
        isFormValid = true;
      })
      .on('core.form.invalid', function () {
        // if fields are invalid
        isFormValid = false;
      });

    // Sidebar Toggle Btn
    if (btnToggleSidebar) {
      btnToggleSidebar.addEventListener('click', e => {
        btnCancel.classList.remove('d-none');
      });
    }

    // Add Event
    // ------------------------------------------------
    function addEvent(eventData) {
      // ? Add new event data to current events object and refetch it to display on calender
      // ? You can write below code to AJAX call success response

      currentEvents.push(eventData);
      calendar.refetchEvents();

      // ? To add event directly to calender (won't update currentEvents object)
      // calendar.addEvent(eventData);
    }

    // Update Event
    // ------------------------------------------------
    function updateEvent(eventData) {
      // ? Update existing event data to current events object and refetch it to display on calender
      // ? You can write below code to AJAX call success response
      eventData.id = parseInt(eventData.id);
      currentEvents[currentEvents.findIndex(el => el.id === eventData.id)] = eventData; // Update event by id
      calendar.refetchEvents();

      // ? To update event directly to calender (won't update currentEvents object)
      // let propsToUpdate = ['id', 'title', 'url'];
      // let extendedPropsToUpdate = ['calendar', 'guests', 'location', 'description'];

      // updateEventInCalendar(eventData, propsToUpdate, extendedPropsToUpdate);
    }

    // Remove Event
    // ------------------------------------------------

    function removeEvent(eventId) {
      // ? Delete existing event data to current events object and refetch it to display on calender
      // ? You can write below code to AJAX call success response
      currentEvents = currentEvents.filter(function (event) {
        return event.id != eventId;
      });
      calendar.refetchEvents();

      // ? To delete event directly to calender (won't update currentEvents object)
      // removeEventInCalendar(eventId);
    }

    // (Update Event In Calendar (UI Only)
    // ------------------------------------------------
    const updateEventInCalendar = (updatedEventData, propsToUpdate, extendedPropsToUpdate) => {
      const existingEvent = calendar.getEventById(updatedEventData.id);

      // --- Set event properties except date related ----- //
      // ? Docs: https://fullcalendar.io/docs/Event-setProp
      // dateRelatedProps => ['start', 'end', 'allDay']
      // eslint-disable-next-line no-plusplus
      for (var index = 0; index < propsToUpdate.length; index++) {
        var propName = propsToUpdate[index];
        existingEvent.setProp(propName, updatedEventData[propName]);
      }

      // --- Set date related props ----- //
      // ? Docs: https://fullcalendar.io/docs/Event-setDates
      existingEvent.setDates(updatedEventData.start, updatedEventData.end, {
        allDay: updatedEventData.allDay
      });

      // --- Set event's extendedProps ----- //
      // ? Docs: https://fullcalendar.io/docs/Event-setExtendedProp
      // eslint-disable-next-line no-plusplus
      for (var index = 0; index < extendedPropsToUpdate.length; index++) {
        var propName = extendedPropsToUpdate[index];
        existingEvent.setExtendedProp(propName, updatedEventData.extendedProps[propName]);
      }
    };

    // Remove Event In Calendar (UI Only)
    // ------------------------------------------------
    function removeEventInCalendar(eventId) {
      calendar.getEventById(eventId).remove();
    }

    // Add new event
    // ------------------------------------------------
    btnSubmit.addEventListener('click', e => {
      if (btnSubmit.classList.contains('btn-add-event')) {
        if (isFormValid) {
          let newEvent = {
            id: calendar.getEvents().length + 1,
            title: eventTitle.value,
            start: eventStartDate.value,
            end: eventEndDate.value,
            startStr: eventStartDate.value,
            endStr: eventEndDate.value,
            categoria: categoria.value,
            tipoEvento: tipoEvento.value,
            localidad: localidad.value,
            display: 'block',
            extendedProps: {
              calendar: tipoEvento.value,
              description: eventDescription.value
            }
          };
          
          if (allDaySwitch.checked) {
            newEvent.allDay = true;
          }
          addEvent(newEvent);
          bsAddEventSidebar.hide();
        }
      } else {
        // Update event
        // ------------------------------------------------
        if (isFormValid) {
          let eventData = {
            id: eventToUpdate.id,
            title: eventTitle.value,
            start: eventStartDate.value,
            end: eventEndDate.value,
            categoria: categoria.value,
            tipoEvento: tipoEvento.value,
            localidad: localidad.value,
            extendedProps: {
              calendar: tipoEvento.value,
              description: eventDescription.value
            },
            display: 'block',
            allDay: allDaySwitch.checked ? true : false
          };

          updateEvent(eventData);
          bsAddEventSidebar.hide();
        }
      }
    });

    // Call removeEvent function
    btnDeleteEvent.addEventListener('click', e => {
      removeEvent(parseInt(eventToUpdate.id));
      // eventToUpdate.remove();
      bsAddEventSidebar.hide();
    });

    // Reset event form inputs values
    // ------------------------------------------------
    function resetValues() {
      eventEndDate.value = '';
      eventStartDate.value = '';
      eventTitle.value = '';
      allDaySwitch.checked = false;
      eventDescription.value = '';
    }

    // When modal hides reset input values
    addEventSidebar.addEventListener('hidden.bs.offcanvas', function () {
      calendar.setOption('locale', 'es');
      resetValues();
    });

    // Hide left sidebar if the right sidebar is open
    btnToggleSidebar.addEventListener('click', e => {
      if (offcanvasTitle) {
        offcanvasTitle.innerHTML = 'Agregar Evento';
      }
      btnSubmit.innerHTML = 'Agregar';
      btnSubmit.classList.remove('btn-update-event');
      btnSubmit.classList.add('btn-add-event');
      btnDeleteEvent.classList.add('d-none');
      appCalendarSidebar.classList.remove('show');
      appOverlay.classList.remove('show');
    });

    // Calender filter functionality
    // ------------------------------------------------
    if (selectAll) {
      selectAll.addEventListener('click', e => {
        if (e.currentTarget.checked) {
          document.querySelectorAll('.input-filter').forEach(c => (c.checked = 1));
        } else {
          document.querySelectorAll('.input-filter').forEach(c => (c.checked = 0));
        }
        calendar.refetchEvents();
      });
    }

    if (filterInput) {
      filterInput.forEach(item => {
        item.addEventListener('click', () => {
          document.querySelectorAll('.input-filter:checked').length < document.querySelectorAll('.input-filter').length
            ? (selectAll.checked = false)
            : (selectAll.checked = true);
          calendar.refetchEvents();
        });
      });
    }

    // Jump to date on sidebar(inline) calendar change
    inlineCalInstance.config.onChange.push(function (date) {
      calendar.changeView(calendar.view.type, moment(date[0]).format('YYYY-MM-DD'));
      modifyToggler();
      appCalendarSidebar.classList.remove('show');
      appOverlay.classList.remove('show');
    });
  })();
});


document.getElementById('eventForm').addEventListener('submit', function (e) {
  e.preventDefault(); // evitar que se envíe el form de forma tradicional

  const formData = new FormData(this);

  document.querySelectorAll('input[name="tipoEventos[]"]:checked').forEach(input => {
    formData.append('tipoEventos[]', input.value);
    });
    for (let pair of formData.entries()) {
      console.log(pair[0]+ ': ' + pair[1]);
    }
  fetch('/calendario/nuevoEvento', {
    method: 'POST',
    body: formData
  })
  .then(response => {
    if (response.ok) {
      // Ocultás el modal y recargás eventos
      calendar.refetchEvents();
      // Ocultar el sidebar si querés
      bsAddEventSidebar.hide();
    } else {
      alert('Error al guardar el evento');
    }
  });
});
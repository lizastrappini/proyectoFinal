'use strict';

var direction = 'ltr';
if (typeof isRtl !== 'undefined' && isRtl) {
  direction = 'rtl';
}

function parseDDMMYYYY_HHmm(str) {
  if (!str) return null;
  const m = str.match(/^(\d{2})-(\d{2})-(\d{4})(?:\s+(\d{2}):(\d{2}))?$/);
  if (!m) return null;
  const [, dd, mm, yyyy, HH = '00', II = '00'] = m;
  return new Date(Number(yyyy), Number(mm) - 1, Number(dd), Number(HH), Number(II));
}

document.addEventListener('DOMContentLoaded', function () {
  
  (function () {
    const calendarEl = document.getElementById('calendar'),
      appCalendarSidebar = document.querySelector('.app-calendar-sidebar'),
      addEventSidebar = document.getElementById('addEventSidebar'),
      appOverlay = document.querySelector('.app-overlay'),
       tipoEventoColor = {
             "1": "primary",
            "2": "success",
            "3": "danger",
            "4": "warning",
            "5": "info",
            "6": "recaudacion",
            "7": "miCategoria"
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

      eventEndDateMasivo = document.querySelector('#eventEndDateMasivo'),
      eventStartDateMasivo = document.querySelector('#eventStartDateMasivo'),
      horaInicioMasivo = document.querySelector('#horaInicioMasivo'),

      contrincante = document.querySelector('#contrincante'),
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
        altInput: true,            // 👈 agrega un input visible
        altFormat: "d-m-Y H:i",    // 👈 lo que ve el usuario
        dateFormat: "Y-m-d H:i:S",  // 👈 lo que se guarda/envía
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
        altInput: true,            // 👈 agrega un input visible
        altFormat: "d-m-Y H:i",    // 👈 lo que ve el usuario
        dateFormat: "Y-m-d H:i:S",   // 👈 lo que se guarda/envía
        onReady: function (selectedDates, dateStr, instance) {
          if (instance.isMobile) {
            instance.mobileInput.setAttribute('step', null);
          }
        }
      });
    }

    if (eventStartDateMasivo) {
      var start = eventStartDateMasivo.flatpickr({
        locale: flatpickr.l10ns.es,
        altInput: true,            // 👈 agrega un input visible
        altFormat: "d-m-Y ",    // 👈 lo que ve el usuario
        dateFormat: "Y-m-d ",   // 👈 lo que se guarda/envía
        minDate: "today",  
        onReady: function (selectedDates, dateStr, instance) {
          if (instance.isMobile) {
            instance.mobileInput.setAttribute('step', null);
          }
        }
      });
    }

    if (eventEndDateMasivo) {
      var end = eventEndDateMasivo.flatpickr({
        locale: flatpickr.l10ns.es,
        altInput: true,            // 👈 agrega un input visible
        altFormat: "d-m-Y ",    // 👈 lo que ve el usuario
        dateFormat: "Y-m-d ",   // 👈 lo que se guarda/envía
        minDate: "today",   
        onReady: function (selectedDates, dateStr, instance) {
          if (instance.isMobile) {
            instance.mobileInput.setAttribute('step', null);
          }
        }
      });
    }


if (horaInicioMasivo) {
  var start = horaInicioMasivo.flatpickr({
    locale: flatpickr.l10ns.es,
    enableTime: true,
    noCalendar: true,         // 👈 solo muestra horas/minutos
    time_24hr: true,          // 👈 formato 24h
    altInput: true,           
    altFormat: "H:i",         // 👈 lo que ve el usuario
    dateFormat: "H:i",        // 👈 lo que se envía al backend
    onReady: function (selectedDates, dateStr, instance) {
      if (instance.isMobile) {
        instance.mobileInput.setAttribute('step', null);
      }
    }
  });
}

  const btnNuevoEventoMasivo = document.getElementById('btnNuevoEventoMasivo');

  if (btnNuevoEventoMasivo) {
    btnNuevoEventoMasivo.addEventListener('click', e => {
      // Limpiar valores del form
      resetValues();
      //bsAddEventSidebar.show();

      // Personalizar modal
      if (offcanvasTitle) {
        offcanvasTitle.innerHTML = 'Agregar Evento Masivo';
      }
      if (btnSubmit) {
        btnSubmit.innerHTML = 'Agregar';
        btnSubmit.classList.remove('btn-update-event', 'btn-add-event');
        btnSubmit.classList.add('btn-add-event-masivo');
      }
      if (btnDeleteEvent) btnDeleteEvent.classList.add('d-none');
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

function mostrarCamposSegunTipo(forceTipo = null, ocultarTipo = false) {
  const tipo = String(forceTipo ?? tipoEvento.value ?? '');

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

  // Mostrar el selector de tipo solo si no estamos en edición
  if (!ocultarTipo && wrappers.tipoEvento) {
    wrappers.tipoEvento.style.display = 'block';
  }

  switch (tipo) {
    case '1': // Entrenamiento
      [wrappers.eventStartDate, wrappers.categoria, wrappers.rama, wrappers.division]
        .forEach(w => w && (w.style.display = 'block'));
      break;

    case '2': // Partido
      [wrappers.categoria, wrappers.eventStartDate,
       wrappers.localidad, wrappers.contrincante, wrappers.rama, wrappers.division]
        .forEach(w => w && (w.style.display = 'block'));
      break;

    case '3': // Vacaciones
      [wrappers.titulo, wrappers.eventStartDate, wrappers.eventEndDate]
        .forEach(w => w && (w.style.display = 'block'));
      break;

    case '4': // Suspension
      [wrappers.titulo, wrappers.eventStartDate, wrappers.categoria, wrappers.rama, wrappers.division]
        .forEach(w => w && (w.style.display = 'block'));
      break;

    case '5': // Torneo
      [wrappers.titulo, wrappers.eventStartDate, wrappers.eventEndDate,
       wrappers.categoria, wrappers.rama, wrappers.division, wrappers.localidad]
        .forEach(w => w && (w.style.display = 'block'));
      break;

    case '6': // Recaudación
      [wrappers.titulo, wrappers.eventStartDate, wrappers.categoria, wrappers.descripcion,wrappers.rama, wrappers.division]
        .forEach(w => w && (w.style.display = 'block'));
      break;
  }
}


    // Event listener
   if (tipoEvento) {
  $(tipoEvento).on('change select2:select', function () {
    mostrarCamposSegunTipo();
  });

  // llamada inicial
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

      // ✅ leemos el rol del data-attribute del calendario
      const userRole = parseInt(idRolUsuario.dataset.userRole || '0', 10);

      if (userRole === 2) {
      if (offcanvasTitle) offcanvasTitle.innerHTML = 'Detalle del Evento';
      if (btnSubmit) btnSubmit.classList.add('d-none');
      if (btnDeleteEvent) btnDeleteEvent.classList.add('d-none');

      const form = document.getElementById('eventForm');
      if (form) form.classList.add('d-none');  
      if (eventDetails) {
        eventDetails.classList.remove('d-none');
        eventDetails.innerHTML = `<p>Cargando...</p>`;
      }

      fetch(`/evento/${eventToUpdate.id}`)
        .then(res => res.json())
        .then(data => {
if (eventDetails) {
  let html = '';

  // título destacado
  if (data.titulo) {
    html += `<h4 class="mb-3 text-center">📆${data.titulo}</h4>`;
  }

  // helper para renderizar solo si hay valor
  const renderField = (label, value) => {
    if (!value) return '';
    return `
      <li class="list-group-item d-flex justify-content-between align-items-center">
        <span class="fw-semibold">${label}</span>
        <span>${value}</span>
      </li>
    `;
  };

  // abrimos la lista
  html += '<ul class="list-group mb-3">';

  html += renderField('Inicio', data.fechaInicio);
  html += renderField('Fin', data.fechaFin);
  html += renderField('Tipo', data.tipoEvento);
  html += renderField('Categoría', data.categoria);
  html += renderField('Rama', data.rama);
  html += renderField('División', data.division);
  html += renderField('Localidad', data.localidad);
  html += renderField('Contrincante', data.contrincante);
  html += renderField('Descripción', data.descripcion);

  // cerramos la lista
  html += '</ul>';

  eventDetails.innerHTML = html || '<p class="text-muted">No hay información disponible.</p>';
}
        });
      return;
  }

// ------- MODO EDICIÓN (Admin/Entrenador) -------
if (offcanvasTitle) offcanvasTitle.innerHTML = 'Actualizar Evento';
if (btnSubmit) {
  btnSubmit.innerHTML = 'Actualizar';
  btnSubmit.classList.add('btn-update-event');
  btnSubmit.classList.remove('btn-add-event', 'd-none');
}
if (btnDeleteEvent) btnDeleteEvent.classList.remove('d-none');

const form = document.getElementById('eventForm');
if (form) {
  form.classList.remove('d-none');
  form.action = `/updateEvento/${eventToUpdate.id}`; // 👈 POST al enviar
}
const inputId = document.getElementById('eventoId');
if (inputId) inputId.value = eventToUpdate.id;

// 👇 GET para obtener datos
fetch(`/evento/${eventToUpdate.id}`)
  .then(res => res.json())
  .then(data => {
    // textos
    if (eventTitle) eventTitle.value = data.titulo || '';
    if (eventDescription) eventDescription.value = data.descripcion || '';

    // selects (IDs)
    if (categoria) $(categoria).val(data.IdCategoria || '').trigger('change');
    if (rama)      $(rama).val(data.IdRama || '').trigger('change');
    if (division)  $(division).val(data.IdDivision || '').trigger('change');
    if (localidad) $(localidad).val(data.IdLocalidad || '').trigger('change');
    if (contrincante) $(contrincante).val(String(data.IdContrincante || '')).trigger('change');
    
    // tipo para decidir wrappers (ocultando el select de tipo)
    const tipoStr = String(data.tipo || '');
    if (tipoEvento) tipoEvento.value = tipoStr;
    mostrarCamposSegunTipo(tipoStr, true);

    // fechas (ISO → Date)
    if (eventStartDate && data.fechaInicioFormat) {
      flatpickr(eventStartDate, {
        locale: flatpickr.l10ns.es,
        enableTime: true,
        altInput: true,
        altFormat: "d-m-Y H:i",
        dateFormat: "Y-m-d H:i:S",
        defaultDate: new Date(data.fechaInicioFormat)
      });
    }
    if (eventEndDate && data.fechaFinFormat) {
      flatpickr(eventEndDate, {
        locale: flatpickr.l10ns.es,
        enableTime: true,
        altInput: true,
        altFormat: "d-m-Y H:i",
        dateFormat: "Y-m-d H:i:S",
        defaultDate: new Date(data.fechaFinFormat)
      });
    }

    if (allDaySwitch) allDaySwitch.checked = !!data.todoElDia;
})
.catch(() => {
  // fallback: mostrar el selector si algo falla
  mostrarCamposSegunTipo('', false);
});

} // 👈 cierra el bloque eventClick para rol 1/3

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
  const allBox = document.querySelector('input[data-value="all"]');
  const checked = document.querySelectorAll('.input-filter:checked');
  let selected = [];

  console.log("todos: ", allBox, "marcados:", checked);
  // Caso 1: solo "Todos" marcado
if (allBox && allBox.checked) {
  // devolver todos los valores de los checkboxes que existan en el DOM
  return [...document.querySelectorAll('.input-filter')].map(cb => cb.value);
}

  // Caso 2: hay específicos marcados
  checked.forEach(item => {
    const val = item.getAttribute('data-value');
    if (val !== 'all') {
      selected.push(val.toLowerCase());
    }
  });

  // Caso 3: ninguno marcado → devuelve vacío
  return selected;
}

const deleteBtn = document.getElementById('deleteEventBtn');
if (deleteBtn) {
  deleteBtn.onclick = () => {
    const id = document.getElementById('eventoId').value;

    Swal.fire({
      title: "¿Estás seguro?",
      text: "Esta acción eliminará el evento permanentemente.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "Sí, eliminar",
      cancelButtonText: "Cancelar",
      reverseButtons: true,
      didOpen: function() {

        document.querySelector('.swal2-container').style.zIndex = 20000;
        document.querySelector('.swal2-popup').style.zIndex = 20001;
    },
    }).then((result) => {
      if (result.isConfirmed) {
        fetch(`/eliminarEvento/${id}`, {
          method: "POST"  // o DELETE si tu backend lo soporta
        })
        .then(() => {
          Swal.fire("Eliminado", "El evento fue eliminado correctamente.", "success");
          calendar.refetchEvents();
          bsAddEventSidebar.hide();
        })
        .catch(() => {
          Swal.fire("Error", "No se pudo eliminar el evento.", "error");
        });
      }
    });
  };
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

      const idRolUsuario = document.getElementById('idRolUsuario');
      const userRole = parseInt(idRolUsuario.dataset.userRole, 10);

    // Init FullCalendar
    // ------------------------------------------------
    let calendar = new Calendar(calendarEl, {
      locale: 'es',
      initialView: 'dayGridMonth',
        eventDisplay: 'block', // fuerza apariencia "block" (no dot)
        eventDidMount: function (info) {
          if (info.view.type !== 'dayGridMonth') return;

          const palette = {
            "1": { bg: 'var(--bs-primary)',  border: 'var(--bs-primary)',  color: '#fff' },
            "2": { bg: 'var(--bs-success)',  border: 'var(--bs-success)',  color: '#fff' },
            "3": { bg: 'var(--bs-danger)',   border: 'var(--bs-danger)',   color: '#fff' },
            "4": { bg: 'var(--bs-warning)',  border: 'var(--bs-warning)',  color: '#000' },
            "5": { bg: 'var(--bs-info)',     border: 'var(--bs-info)',     color: '#000' },
            "6": { bg: '#9b59b6',            border: '#8e44ad',            color: '#fff' }, // Recaudación
            "7": { bg: '#d47a13',            border: '#d47a13',            color: '#fff' }  // MiCategoría
          };

          const tipo = String(info.event.extendedProps.calendar);
          const p = palette[tipo];
          if (!p) return;

          // 🎨 Aplicar solo al contenedor
          info.el.style.backgroundColor = p.bg;
          info.el.style.borderColor = p.border;
          info.el.style.color = p.color;

          // Por si FC usa variables CSS
          info.el.style.setProperty('--fc-event-bg-color', p.bg);
          info.el.style.setProperty('--fc-event-border-color', p.border);

          // Texto: aseguramos contraste
          const main = info.el.querySelector('.fc-event-main');
          if (main) main.style.color = p.color;

          // Extras que ya tenías
          info.el.style.overflow = 'hidden';
          info.el.style.maxWidth = '100%';
          info.el.style.borderRadius = '4px';

          const frame = info.el.querySelector('.fc-event-main-frame');
          if (frame) frame.style.display = 'block';

          const title = info.el.querySelector('.fc-event-title');
          if (title) {
            title.style.whiteSpace = 'normal';
            title.style.wordBreak = 'break-word';
            title.style.lineHeight = '1.2';
          }

          if (tipo === "7") {
            const miCatCheck = document.querySelector('#select-miCategoria');
            if (miCatCheck && miCatCheck.checked) {
              info.el.style.backgroundColor = '#d47a13';
              info.el.style.borderColor = '#d47a13';
              info.el.style.color = '#000';
            } else {
              // si el checkbox no está marcado, que quede sin color
              info.el.style.backgroundColor = '';
              info.el.style.borderColor = '';
              info.el.style.color = '';
            }
          }
        },
        height: '100%',        // ocupa todo el espacio de su columna
      contentHeight: 'auto', // se adapta al alto disponible
      handleWindowResize: true,
       displayEventTime: false,
       buttonText: {
        dayGridMonth: 'Mes',
        listMonth: 'Lista'
      },
      viewDidMount: function(info) {
    if (info.view.type === 'listMonth') {
      // Limitar alto solo para listMonth
      info.el.querySelector('.fc-scroller').style.maxHeight = '600px';
      info.el.querySelector('.fc-scroller').style.overflowY = 'auto';
    } else {
      // En otras vistas lo dejamos normal
      info.el.querySelector('.fc-scroller').style.maxHeight = '';
      info.el.querySelector('.fc-scroller').style.overflowY = '';
    }
  },
      eventColor: null,
eventBackgroundColor: null,
eventBorderColor: null,
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
      console.log("extraParams (rol 2):", params);
      return params;
    }
  },
      plugins: [dayGridPlugin, interactionPlugin, listPlugin, timegridPlugin],
      editable: true,
      dragScroll: true,
      dayMaxEvents: 1,
      moreLinkText: function(n) {
        return "+ ver " + n + " más";
      },
      eventResizableFromStart: true,
      customButtons: {
        sidebarToggle: {
          text: 'Sidebar'
        }
      },
      headerToolbar: {
        locale: 'es',
        start: 'sidebarToggle, prev,next, title',
        end: 'dayGridMonth,listMonth'
      },
      direction: direction,
      initialDate: new Date(),
      navLinks: true, // can click day/week names to navigate views
      eventClassNames: function ({ event: calendarEvent }) {
  const tipo = String(calendarEvent.extendedProps.calendar);
  const colorClass = tipoEventoColor[tipo];
  console.log("tipo:", tipo, "clase:", colorClass);
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
console.log("calendarEl:", calendarEl);
    // Render calendar
    calendar.render();
    // Modify sidebar toggler
    modifyToggler();

    const eventForm = document.getElementById('eventForm');
if (eventForm && typeof FormValidation !== 'undefined') {
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
       .on('core.form.valid', () => { isFormValid = true; })
    .on('core.form.invalid', () => { isFormValid = false; });
  }

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
    if (btnSubmit) {
      btnSubmit.addEventListener('click', e => {
        if (btnSubmit.classList.contains('btn-add-event')) {
          if (isFormValid) {
            let newEvent = {
              
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
    }
    if (btnDeleteEvent) {
      // Call removeEvent function
      btnDeleteEvent.addEventListener('click', e => {
        removeEvent(parseInt(eventToUpdate.id));
        // eventToUpdate.remove();
        bsAddEventSidebar.hide();
      });
    }
    // Reset event form inputs values
    // ------------------------------------------------
    // === RESET FORM ===
function resetValues() {
  // inputs básicos
  if (eventEndDate) eventEndDate.value = '';
  if (eventStartDate) eventStartDate.value = '';
  if (eventTitle) eventTitle.value = '';
  if (eventDescription) eventDescription.value = '';
  if (allDaySwitch) allDaySwitch.checked = false;

  // selects con select2
  if (categoria) $(categoria).val(null).trigger('change');
  if (rama) $(rama).val(null).trigger('change');
  if (division) $(division).val(null).trigger('change');
  if (localidad) $(localidad).val(null).trigger('change');
  if (contrincante) $(contrincante).val(null).trigger('change');
  if (tipoEvento) $(tipoEvento).val(null).trigger('change');

  // hidden id
  const inputId = document.getElementById('eventoId');
  if (inputId) inputId.value = '';
}
addEventSidebar.addEventListener('hidden.bs.offcanvas', function () {
  resetValues();
});

// === ABRIR MODAL DESDE BOTÓN (NUEVO EVENTO) ===
if (btnToggleSidebar) {
  btnToggleSidebar.addEventListener('click', function () {
    resetValues();

    let offcanvas = bootstrap.Offcanvas.getInstance(addEventSidebar);
    if (!offcanvas) {
      offcanvas = new bootstrap.Offcanvas(addEventSidebar);
    }
    if (!addEventSidebar.classList.contains('show')) {
      offcanvas.show();
    }
  });
}

// === DATECLICK (NUEVO EVENTO DESDE CALENDARIO) ===
calendar.on('dateClick', function (info) {
  resetValues();
  eventStartDate.value = info.dateStr;
  eventEndDate.value = info.dateStr;

  let offcanvas = bootstrap.Offcanvas.getInstance(addEventSidebar);
  if (!offcanvas) {
    offcanvas = new bootstrap.Offcanvas(addEventSidebar);
  }
  if (!addEventSidebar.classList.contains('show')) {
    offcanvas.show();
  }
});


    // Hide left sidebar if the right sidebar is open
    if (btnToggleSidebar) {
      btnToggleSidebar.addEventListener('click', e => {
        if (offcanvasTitle) offcanvasTitle.innerHTML = 'Agregar Evento';
        if (btnSubmit) {
          btnSubmit.innerHTML = 'Agregar';
          btnSubmit.classList.remove('btn-update-event');
          btnSubmit.classList.add('btn-add-event');
        }
        if (btnDeleteEvent) btnDeleteEvent.classList.add('d-none');
        appCalendarSidebar.classList.remove('show');
        appOverlay.classList.remove('show');
      });
    }

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



window.addEventListener('load', () => {
    const userBirthDate = document.querySelector('#user-birthdate-input');
    const userDate = document.querySelector('#user-age-input');
    const userBirthDate2 = document.querySelector('#user-birthdate-input2');
    const userDate2 = document.querySelector('#user-age-input2');
    const userDisability = document.querySelectorAll("input[name='radio-discapacidad']");
    const agresorDisability = document.querySelectorAll("input[name='radio-relation']");
    const denunciaDisability = document.querySelectorAll("input[name='radio-denuncia']");
    const referidaDisability = document.querySelectorAll("input[name='radio-referida']");


    const violenceOther = document.querySelector('#checkbox-type-violence-other');
    const inputviolenceOther = document.querySelector('.type-violence-other');
    const placeOther = document.querySelector('#checkbox-place-other');
    const inputplaceOther = document.querySelector('.place-violence-other');
    const yesComplaint = document.querySelector('#checkbox-yes-complaint');
    const historyViolence = document.querySelector('.history-violence');
    const physicalOther = document.querySelector('#checkbox-physical-violence-other');
    const inputphysicalOther = document.querySelector('.physical-violence-other');
    const emotionalOther = document.querySelector('#checkbox-emotional-violence-other');
    const inputemotionalOther = document.querySelector('.emotional-violence-other');
    const sexualOther = document.querySelector('#checkbox-sexual-violence-other');
    const inputsexualOther = document.querySelector('.sexual-violence-other');
    const economicOther = document.querySelector('#checkbox-economic-violence-other');
    const inputeconomicOther = document.querySelector('.economic-violence-other');
    const serviceOther = document.querySelector('#checkbox-other-service');
    const inputserviceOther = document.querySelector('.service-violence-other');

    const checkboxmmsr = document.querySelector('#checkbox-mmsr');
    const checkboxmae = document.querySelector('#checkbox-mae');
    const checkboxmaa = document.querySelector('#checkbox-maa');
    const checkboxconecta = document.querySelector('#checkbox-conecta');
    const checkboxpolicia = document.querySelector('#checkbox-policia');
    const checkboxministerio = document.querySelector('#checkbox-ministerio');
    const checkboxsesal = document.querySelector('#checkbox-sesal');
    const checkboxsecretaria = document.querySelector('#checkbox-secretaria');
    const checkboxdinaf = document.querySelector('#checkbox-dinaf');
    const checkboxalbergue = document.querySelector('#checkbox-albergue');
    const checkboxong = document.querySelector('#checkbox-ong');
    const checkboxotro = document.querySelector('#checkbox-otro');

    const checkboxmmsrOther = document.querySelector('.checkbox-mmsr-other');
    const checkboxmaerOther = document.querySelector('.checkbox-mae-other');
    const checkboxmaarOther = document.querySelector('.checkbox-maa-other');
    const checkboxconectaOther = document.querySelector('.checkbox-conecta-other');
    const checkboxpoliciaOther = document.querySelector('.checkbox-policia-other');
    const checkboxministerioOther = document.querySelector('.checkbox-ministerio-other');
    const checkboxsesalOther = document.querySelector('.checkbox-sesal-other');
    const checkboxsecretariaOther = document.querySelector('.checkbox-secretaria-other');
    const checkboxdinafOther = document.querySelector('.checkbox-dinaf-other');
    const checkboxalbergueOther = document.querySelector('.checkbox-albergue-other');
    const checkboxongOther = document.querySelector('.checkbox-ong-other');
    const checkboxotroOther = document.querySelector('.checkbox-otro-other');

    const functionApearInput = (checkChange, inputLabel) => {
        checkChange.addEventListener('change', () => {
            if(checkChange.checked){
                inputLabel.classList.remove('container--hidden');
            } else {
                inputLabel.classList.add('container--hidden');
            }
        });
    }

    functionApearInput(checkboxpolicia, checkboxpoliciaOther);
    functionApearInput(checkboxministerio, checkboxministerioOther);
    functionApearInput(checkboxsesal, checkboxsesalOther);
    functionApearInput(checkboxsecretaria, checkboxsecretariaOther);
    functionApearInput(checkboxdinaf, checkboxdinafOther);
    functionApearInput(checkboxalbergue, checkboxalbergueOther);
    functionApearInput(checkboxong, checkboxongOther);
    functionApearInput(checkboxotro, checkboxotroOther);


    checkboxmmsr.addEventListener('change', () => {
        if(checkboxmmsr.checked){
            checkboxmmsrOther.classList.remove('container--hidden');
        } else {
            checkboxmmsrOther.classList.add('container--hidden');
        }
    });

    checkboxmaa.addEventListener('change', () => {
        if(checkboxmaa.checked){
            checkboxmaarOther.classList.remove('container--hidden');
        } else {
            checkboxmaarOther.classList.add('container--hidden');
        }
    });

    checkboxmae.addEventListener('change', () => {
        if(checkboxmae.checked){
            checkboxmaerOther.classList.remove('container--hidden');
        } else {
            checkboxmaerOther.classList.add('container--hidden');
        }
    });

    checkboxconecta.addEventListener('change', () => {
        if(checkboxconecta.checked){
            checkboxconectaOther.classList.remove('container--hidden');
        } else {
            checkboxconectaOther.classList.add('container--hidden');
        }
    });

    const btnAGresor = document.querySelector('.btn-agresor');
    

    const containerForm1 = document.querySelector('.container-form-1');
    const containerForm2 = document.querySelector('.container-form-2');
    const containerForm3 = document.querySelector('.container-form-3');
    const containerForm31 = document.querySelector('.container-form-3-1');

    const containerForm4 = document.querySelector('.container-form-4');
    const buttonForm1 = document.querySelector('#btn-form-1');
    const buttonForm2 = document.querySelector('#btn-form-2');
    const buttonForm3 = document.querySelector('#btn-form-3');
    const buttonForm4 = document.querySelector('#btn-form-4');

    let haveDisability = 'no';

    btnAGresor.addEventListener('click', () => {
        containerForm31.classList.remove('container--hidden');
    });

    const calcularEdad = (fechaNacimiento) => {
        const fechaActual = new Date();
        const anoActual = parseInt(fechaActual.getFullYear());
        const mesActual = parseInt(fechaActual.getMonth());
        const diaActual = parseInt(fechaActual.getDate());

        // date format 2022-12-06
        const anoNacimiento = parseInt(String(fechaNacimiento).substring(0, 4));
        const mesNacimiento = parseInt(String(fechaNacimiento).substring(5, 7));
        const diaNacimiento = parseInt(String(fechaNacimiento).substring(8, 10));

        let edad = anoActual - anoNacimiento;
        if(mesActual < mesNacimiento) {
            edad--;
        } else if (mesActual === mesNacimiento) {
            if(diaActual < diaNacimiento) {
                edad--;
            } 
        } 
        return edad < 0 ? 0 : edad;
    }

    let findSelected = () => {
        let selected = document.querySelector("input[name='radio-discapacidad']:checked");

    } 

    userBirthDate.addEventListener('change', () => {
        if(userBirthDate.value) {
            userDate.value = calcularEdad(userBirthDate.value);
        }
    })

    userBirthDate2.addEventListener('change', () => {
        if(userBirthDate2.value) {
            userDate2.value = calcularEdad(userBirthDate2.value);
        }
    })

    userDisability.forEach(elem => {
        elem.addEventListener('change', () => {
            const containerDisability = document.querySelector('.container-disability');
            haveDisability= elem.value;
            
            if(elem.value == 'si'){
                containerDisability.classList.remove('container--hidden');
            } else {
                containerDisability.classList.add('container--hidden');
            }
        })
    });

    agresorDisability.forEach(elem => {
        elem.addEventListener('change', () => {
            const containerDisability = document.querySelector('.container-other-agresor');
            if(elem.value == 'otro'){
                containerDisability.classList.remove('container--hidden');
            } else {
                containerDisability.classList.add('container--hidden');
            }
        })
    });

    denunciaDisability.forEach(elem => {
        elem.addEventListener('change', () => {
            const containerDisability = document.querySelector('.history-violence');
            if(elem.value == 'Si'){
                containerDisability.classList.remove('container--hidden');
            } else {
                containerDisability.classList.add('container--hidden');
            }
        })
    });

    referidaDisability.forEach(elem => {
        elem.addEventListener('change', () => {
            const containerMmsrDisability = document.querySelector('.checkbox-mmsr-other');
            const containerMaeDisability = document.querySelector('.checkbox-mae-other');
            const containerMaaDisability = document.querySelector('.checkbox-maa-other');
            const containerConectaDisability = document.querySelector('.checkbox-conecta-other');

            if(elem.value == 'MSSR'){
                containerMmsrDisability.classList.remove('container--hidden');
                containerMaeDisability.classList.add('container--hidden');
                containerMaaDisability.classList.add('container--hidden');
                containerConectaDisability.classList.add('container--hidden');
            } else if (elem.value == 'MAE') {
                containerMaeDisability.classList.remove('container--hidden');
                containerMmsrDisability.classList.add('container--hidden');
                containerMaaDisability.classList.add('container--hidden');
                containerConectaDisability.classList.add('container--hidden');
            } else if (elem.value == 'MAA') {
                containerMaaDisability.classList.remove('container--hidden');
                containerMaeDisability.classList.add('container--hidden');
                containerMmsrDisability.classList.add('container--hidden');
                containerConectaDisability.classList.add('container--hidden');
            } else if ( elem.value == 'CONECTA'){
                containerConectaDisability.classList.remove('container--hidden');
                containerMaeDisability.classList.add('container--hidden');
                containerMaaDisability.classList.add('container--hidden');
                containerMmsrDisability.classList.add('container--hidden');
            } 
        })
    });

    buttonForm1.addEventListener('click', () => {
        containerForm1.classList.add('container--hidden');
        containerForm2.classList.remove('container--hidden');
    });

    violenceOther.addEventListener('change', () => {
        if(violenceOther.checked){
            inputviolenceOther.classList.remove('container--hidden');
        } else {
            inputviolenceOther.classList.add('container--hidden');
        }
    });

    placeOther.addEventListener('change', () => {
        if(placeOther.checked){
            inputplaceOther.classList.remove('container--hidden');
        } else {
            inputplaceOther.classList.add('container--hidden');
        }
    });

    yesComplaint.addEventListener('change', () => {
        if(yesComplaint.checked){
            historyViolence.classList.remove('container--hidden');
        } else {
            historyViolence.classList.add('container--hidden');
        }
    });
    
    physicalOther.addEventListener('change', () => {
        if(physicalOther.checked){
            inputphysicalOther.classList.remove('container--hidden');
        } else {
            inputphysicalOther.classList.add('container--hidden');
        }
    });

    emotionalOther.addEventListener('change', () => {
        if(emotionalOther.checked){
            inputemotionalOther.classList.remove('container--hidden');
        } else {
            inputemotionalOther.classList.add('container--hidden');
        }
    });

    sexualOther.addEventListener('change', () => {
        if(sexualOther.checked){
            inputsexualOther.classList.remove('container--hidden');
        } else {
            inputsexualOther.classList.add('container--hidden');
        }
    });

    economicOther.addEventListener('change', () => {
        if(economicOther.checked){
            inputeconomicOther.classList.remove('container--hidden');
        } else {
            inputeconomicOther.classList.add('container--hidden');
        }
    });

    serviceOther.addEventListener('change', () => {
        if(serviceOther.checked){
            inputserviceOther.classList.remove('container--hidden');
        } else {
            inputserviceOther.classList.add('container--hidden');
        }
    });

    buttonForm2.addEventListener('click', () => {
        containerForm2.classList.add('container--hidden');
        containerForm3.classList.remove('container--hidden');
    });

    buttonForm3.addEventListener('click', () => {
        containerForm3.classList.add('container--hidden');
        containerForm4.classList.remove('container--hidden');
    });
});
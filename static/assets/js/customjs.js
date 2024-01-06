
$(document).ready(function(){
    
    
    // laoder
    
    // body_loader.hide()
    // let element = lv.create($('#lv_loader')[0])
    // element.hide()
    // console.log('type of div loader',typeof element)
    // console.log(' div loader', element)
    //end loader


    //check uppercase
    function hasUpperCase(inputStr) {
        result=false;
    
        let expression=/(?=.*[A-Z])/;
        if(inputStr.match(expression))
        {
            console.log("Upper case letter found");
            result=true;
        }
        return result;
    }
    //validate email
    function ValidateEmail(emailId)
        {
        let mailformat = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
            if(emailId.match(mailformat)){
                //console.log("Valid Email");    
                return true;
            }
            else{
               // console.log("Invalid Email");    
                return false;
            }
        }
        // delay ajax
    let delay = (function () {
        let timer = 0;
        return function (callback, ms) {
          clearTimeout(timer);
          timer = setTimeout(callback, ms);
        };
      })();
    // user register form
    let input = $('#user-register #id_username')
    let error =[]
    input.on('keyup ',function(e){
    user_exist = false
    let username = input.val()
    
    delay(function(){
        $.ajax({
            url: "/account/is-user-exist/",
            data: { 'username': username },
            method: 'POST',
            beforeSend: () => {
              
            },
            success: (result) => {
             
              if (result === true){
                console.log('user exist')
                $('#id_username').addClass('is-invalid')
                error.push('username already exist')
                user_exist=true
                return user_exist
                
               
              }
              else{
                console.log('username available')
                user_exist=false
                $('#id_username').removeClass('is-invalid').addClass('is-valid')
                return user_exist
              }
            },
            complete: () => {
             
            },
          });
    },1000)
   })

   let form = $('#user-register')
   form.on('submit', function(e){
    let user_type=$('#id_user_type').val()
    console.log('user type',user_type)
    let error=[]
    let first_name = user_type ==="supplier"? user_type: $('#id_first_name').val()
    let last_name =  user_type ==="supplier"? user_type: $('#id_last_name').val()
    let username = $('#id_username').val()
    let password = $('#id_password').val()
    let comfirm_password = $('#id_password2').val()
    
    console.log('first name',first_name)
    console.log('last name',last_name)
    
    if (user_exist === true){
        console.log('usename in used')
        error.push('username in  use')
        $('#id_username').addClass('is-invalid')
        // return false
    }
    if(username.length < 4 ){
        error.push('username should be atleast four characters')
        $('#id_username').addClass('is-invalid')
        // return false
    }
    if(first_name.length < 3 ){
        error.push('first name should be atleast three characters')
        $('#id_first_name').addClass('is-invalid')
        // return false
    }
    if(last_name.length < 3 ){
        error.push('last name should be atleast three characters')
        $('#id_last_name').addClass('is-invalid')
        // return false
    }
    if (hasUpperCase(password)=== false ){
        error.push('password must contain atleast on uppercase')
        
        
        $('#id_password').addClass('is-invalid')
        // return false
    }
    if (password !== comfirm_password){
        error.push('Password not match')
        console.log('Password not match')
        $('#id_password2').addClass('is-invalid')
        // return false
    }

    
    if(error.length>0){
        let temp=``
        console.log('cannot submit')
        
        for(let i=0;i < error.length;i++){
            temp+=`<li class="text-danger">${error[i]}</li>`
        }
        console.log(temp)
        $('#error').html(temp)
        return false
    }
   })
   

   //Department and Unit


   $('#id_depart').change(function(){
    let url = '/account/get-unit/';  ///$('#department').attr('unit_urls');
    let department= $(this).val()
    console.log('Department',department)
    $.ajax({
        url:url,
        data:{'dept_id':department},
        success:(data)=>{
            console.log(data)
          
            $('#id_user_unit').html(data)
       
            
        }

    })
})
   //end of depart and Unit
 
   //Search user ajax
    let search_input = $('#id_search')
    search_input.on('keyup',function(e){
        
        search_value = search_input.val()
        //console.log(search_value)
        let template=``
       
            delay(function(){
                $('#form-cont').hide()
            $.ajax({
                url: "/saving/",
                data: { 'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(), 
                'search': search_value },
                method: 'POST',
                beforeSend: () => {
                  
                },
                success: (data) => {
                 if (data != null || undefined){
                    console.log(data)
                   let render_template = data.ipps_no? 
                   template +=`
                   ${data.first_name} | ${data.last_name} | ${data.ipps_no}
               `
                   :''
                    $('#user').html(render_template)
                 }
                 else{
                    console.log('no data')
                    $('#user').html(`<small>Not foun</small>`)
                    $('#form-cont').hide()
                 }
                  
                },
                complete: () => {
                 
                },
              });
        },1000)
       
    })

   // end search user
    // get data
    let linkbtn = $('#get_data')
    linkbtn.on('click',function(e){
        e.preventDefault();
        console.log('click link')

        $('#form-cont').show()

    })

    // end of get data
    
    //save data button
    let form_cont =$('#form-cont')
    form_cont.on('submit',function(e){
        e.preventDefault();
        console.log('save click')
        let contribution = $('#id_contribution').val()
        console.log('contribution',contribution)
        console.log('member',$('#user-register #id_search').val())
        $.ajax({
            url:'/saving/add/',
            data:{
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
                'member_ippis':$('#user-register #id_search').val(),
                'contribution': contribution,
            },
            method:'POST',
            beforeSend: () => {
                  
                },
             success: (res) => {
                
                  console.log(res)
                  message =res.status==="exists"?`Saving for the member ${$('#id_search').val()} already exists.`: `
                   
                   ${res.contribution} for ${res.ippis_no} for  ${res.month}/${res.year} was added successfully
                  
                  `

                $('#id_toast').html(message)
                $('#id_contribution').val(0)
                //   Toastify({

                //     text: "This is a toast",
                    
                //     duration: 3000,
                //     offset: {
                //         x: 50, // horizontal axis - can be a number or a string indicating unity. eg: '2em'
                //         y: 10 // vertical axis - can be a number or a string indicating unity. eg: '2em'
                //       },
                    
                //     }).showToast();
                $('.toast').toast('show');
                 
                },
                complete: () => {
                 
                },

        })
    })
    //end of saved data button

    //profit share page

    let profit_share_form = $('#profitShare')
    $('#id_bene').hide()
    let show_form_btn= $('#add_profit_id')
    show_form_btn.on('click',function(e){
        console.log('click add profit')
        $('#profitShare').show()
    })
    profit_share_form.on('submit',function(e){
        e.preventDefault()
        console.log('profit share submitted')
        let monthly_profit = $('#profitShare #id_profit').val()
        let month = $('#profitShare #id_month').val()
        let year = $('#profitShare #id_year').val()
       
        let form_show=true
        console.log('profit',monthly_profit)
        console.log('month',month)
        console.log('year',year)
        $.ajax({
            url:'/saving/profit/',
            method:'POST',
            data:{'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
            'profit':monthly_profit,
            'month':month,
            'year':year
            },
            beforeSend:function(){
                // saving_form_loader.show()
            },
            success:function(data){
                    //console.log(data)
                    // saving_form_loader.hide()
                    if(Array.isArray(data)){
                        
                    $('#profitShare #id_profit').val('')
                     $('#profitShare #id_month').val('')
                    $('#profitShare #id_year').val('')
                   $('#id_bene').show()
                    let profit_message =`
                    A total profit of ${monthly_profit} for the month of ${month}/${year} was shared successfully.
                    `
                    $('#profit_toast').html(profit_message)
                    $('.toast').toast('show');
                    $('#profitShare').hide()

                    //tabulator
                    let table = new Tabulator("#profit_list", {
                        layout:"fitColumns",
                        pagination:"local",
                        paginationSize:20,
                        paginationSizeSelector:[5,10,15,30],
                        movableColumns:true,
                        paginationCounter:"rows",
                        movableRows:true,
                        rowFormatter:function(row){
                            let row_data = row.getData()
                            if (row_data.col <=0){
                                row.getElement().style.backgroundColor ='red'
                            }
                        },
                        columns:[
                            {title:"Name", headerFilter:true, field:"member_name", sorter:"string"},
                            {title:"IPPIS", headerFilter:true, field:"ippis", sorter:"numeric", headerFliter:true},
                            {title:"Month", field:"month", sorter:"numeric"},
                            {title:"Year", field:"year", sorter:"numeric"},
                            {title:"Unit Profit", field:"unit_profit", sorter:"numeric"},
                            {title:"Member Total Share", field:"total_share_at_month", sorter:"numeric"},
                            {title:"Member Profit", field:"member_profit", sorter:"numeric",formatter:"money", formatterParams:{
                                decimal:".",
                                thousand:",",
                                symbol:"N",
                                
                                precision:2,
                            }},
                        ],
                        data:data,
                       
                        
                    });
                    // end tabulator
                    }
                    else{
                        //console.log('no data')
                        let msg =`${data.data}`
                        $('#profit_toast').html(msg)
                    $('.toast').toast('show');
                    }
            },
            complete:function(){

            },
            error:function(err){
                console(err)
            }
        })

    })
    // end of profit share

    //display saving
    display_default_saving()
    // end of display saving

    //filter saving form
//  let loader = new lv();loader
//     loader.initLoaderAll();
//     loader.startObserving();
 let saving_form_filter =$('#saving_search_form')
//  let saving_form_loader = lv.create($('#saving_form_loder_id')[0])
 //      
  saving_form_filter.on('submit',(e)=>{
      let month = $('#id_month').val()
      let year = $('#id_year').val()
      let ippis = $('#id_ippis').val()
     
      e.preventDefault()
      
      data={
          'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
          'month':month,
          'year':year,
          'ippis':ippis
      }
      //console.log(data)
      $.ajax({
          url:'/saving/saving/',
          method:'POST',
          dataType:'json',
          data:data,
          beforeSend:()=>{
            // saving_form_loader.show()
          },
          success:(data,stu,xhr)=>{
            // saving_form_loader.hide()
            //   console.log('data',data)

            //   console.log(stu)
                 $('#id_month').val('')
                $('#id_year').val('')
                $('#id_ippis').val('')
            
              if (stu==='success' && data.length >0){
                let search_message = `
                Result found for the search
                `
                $('#month_saving_title').html(search_message)
                 var table = new Tabulator('#savings_div',{
                    
                     renderHorizontal:"virtual",
                     pagination:true,
                     paginationSize:20,
                     paginationSizeSelector:[5,10,15,20,25,30],
                     movableColumns:true,
                     paginationCounter:"rows",
                     movableRows:true,
                     rowFormatter:function(row){
                        let row_data = row.getData()
                        if (row_data.col <=0){
                            row.getElement().style.backgroundColor ='red'
                        }
                    },
                     columns:[
                        
                         {title:'Personal Info',
                         columns:[
                             {title:"First name", headerFilter:true, field:"first_name", sorter:"string",},
                             {title:"Last name", headerFilter:true, field:"last_name", sorter:"number" },
                             {title:"IPPIS", headerFilter:true, field:"ippis_no", sorter:"number" },
                         ],
                         frozen:true
                     },
                     {
                         title:'Contribution',
                         columns:[
                             {title:"Month", headerFilter:true, field:"month", sorter:"number" },
                             {title:"Year", headerFilter:true, field:"year", sorter:"number"},
                             {title:"Contribution", headerFilter:true, field:"contribution", sorter:"number" ,formatter:"money", formatterParams:{
                                decimal:".",
                                thousand:",",
                                symbol:"N",
                                
                                precision:2,
                            }},
                             {title:"Monthly Cont.", headerFilter:true, field:"monthly_contribution", sorter:"number" ,formatter:"money", formatterParams:{
                                decimal:".",
                                thousand:",",
                                symbol:"N",
                                
                                precision:2,
                            },
                            topCalc:"sum", topCalcParams:{
                                precision:2,
                            }
                        },//topCalc:'sum'
                             {title:"Saving", headerFilter:true, field:"saving_70", sorter:"number",formatter:"money", formatterParams:{
                                decimal:".",
                                thousand:",",
                                symbol:"N",
                                
                                precision:2,
                            } },
                             {title:"Cumm. Saving", headerFilter:true, field:"cummulative_saving", sorter:"number" ,formatter:"money", formatterParams:{
                                decimal:".",
                                thousand:",",
                                symbol:"N",
                                
                                precision:2,
                            }},
                             {title:"Investment", headerFilter:true, field:"investment", sorter:"number",formatter:"money", formatterParams:{
                                decimal:".",
                                thousand:",",
                                symbol:"N",
                                
                                precision:2,
                            } },
                             {title:"Cumm. Investment", headerFilter:true, field:"cummulative_investment", sorter:"number" ,formatter:"money", formatterParams:{
                                decimal:".",
                                thousand:",",
                                symbol:"N",
                                
                                precision:2,
                            }},
                         ]
                     },
                        {
                         title:'Share',
                         columns:[
                             {title:"Share", headerFilter:true, field:"share", sorter:"number"},
                             {title:"Total Balance", headerFilter:true, field:"total_balance", sorter:"number",formatter:"money",formatterParams:{
                                decimal:".",
                                thousand:".",
                                symbol:"N",
                                
                                precision:2,
                            },
                            
                        },
                             {title:"Cumm. Share", headerFilter:true, field:"cummulative_share", sorter:"number",
                             topCalc:"sum", topCalcParams:{
                                precision:2,
                            },
                            sorter:"number",formatter:"number",formatterParams:{
                                decimal:".",
                                thousand:".",
                                symbol:"#",
                                
                                precision:2,
                            }
                            },
                            
                         ]
                        },
                     ],
                     data:data
                 })
                 $("#download-xlsx").on("click", function(e){
                    e.preventDefault()
                    table.download("xlsx",  `${ippis-year-month}.xlsx`, {sheetName:"My Data"});
                });
                
                //trigger download of data.pdf file
                $("#download-pdf").on("click", function(e){
                    e.preventDefault()
                    table.download("pdf", `${ippis-year-month}.pdf`, {
                        orientation:"lanscape", //set page orientation to portrait
                        title:" Report", //add title to report
                    });
                });
              }
              else{
                let search_message = `
                No result was found
                `
                $('#month_saving_title').html(search_message)
                 display_default_saving()
              }
          },
          complete:()=>{
 
          }
      })
      console.log('saving filter submitted')
     
  })
  //filter saving form

  //saving upload
//   $('#saving_upload_id').on('submit',function(e){
//     e.preventDefault()
//     console.log('saving uplo')
//   })


//members list


})


function display_default_saving(){
    
   
    $.get('/saving/saving/',function(res){
       
       
    let savint_table = new Tabulator('#savings_div',{
        rowFormatter:function(row){
            if(row.getData().col == "blue"){
                row.getElement().style.backgroundColor = "#1e3b20";
            }
        },
        renderHorizontal:"virtual",
        pagination:true,
        paginationSize:20,
        paginationSizeSelector:[5,10,15,20,25,30],
        movableColumns:true,
        paginationCounter:"rows",
        movableRows:true,
        
        columns:[
            
            {title:'Personal Info',
            columns:[
                {title:"First name", headerFilter:true, field:"first_name", sorter:"string",  
            },
                {title:"Last name", headerFilter:true, field:"last_name", sorter:"number" },
                {title:"IPPIS", headerFilter:true, field:"ippis_no", sorter:"number" },
            ],
            frozen:true
        },
        {
            title:'Contribution',
            columns:[
                {title:"Month", headerFilter:true, field:"month", sorter:"number", },
                {title:"Year", headerFilter:true, field:"year", sorter:"number"},
                {title:"Contribution", headerFilter:true, field:"contribution", sorter:"number" , formatter:function(cell, formatterParams){
                    var value = cell.getValue();
                     if(value == '0'){
                         return "<span style='color:#3FB449; font-weight:bolder;background-color:red;'>" + value + "</span>";
                     }else{
                         return value;
                     }
                 },formatter:"money", formatterParams:{
                    decimal:".",
                    thousand:",",
                    symbol:"N",
                    
                    precision:2,
                }},
                {title:"Monthly Cont.", headerFilter:true, field:"monthly_contribution", sorter:"number" ,formatter:"money", formatterParams:{
                    decimal:".",
                    thousand:",",
                    symbol:"N",
                    
                    precision:2,
                },
                topCalc:"sum", topCalcParams:{
                    precision:2,
                }
            },//topCalc:'sum'
                {title:"Saving", headerFilter:true, field:"saving_70", sorter:"number" ,formatter:"money", formatterParams:{
                    decimal:".",
                    thousand:",",
                    symbol:"N",
                    
                    precision:2,
                }},
                {title:"Cumm. Saving", headerFilter:true, field:"cummulative_saving", sorter:"number" ,formatter:"money",formatterParams:{
                    decimal:".",
                    thousand:",",
                    symbol:"N",
                    
                    precision:2,
                }},
                {title:"Investment", headerFilter:true, field:"investment", sorter:"number" ,formatter:"money", formatterParams:{
                    decimal:".",
                    thousand:",",
                    symbol:"N",
                    
                    precision:2,
                }},
                {title:"Cumm. Investment", headerFilter:true, field:"cummulative_investment", sorter:"number" ,formatter:"money",formatterParams:{
                    decimal:".",
                    thousand:",",
                    symbol:"N",
                    
                    precision:2,
                }},
            ]
        },
           {
            title:'Share',
            columns:[
                {title:"Share", headerFilter:true, field:"share", sorter:"number"},
                {title:"Total Balance", headerFilter:true, field:"total_balance", sorter:"number",formatter:"money",formatterParams:{
                    decimal:".",
                    thousand:",",
                    symbol:"N",
                    
                    precision:2,
                },
               
            },
                {title:"Cumm. Share", headerFilter:true, field:"cummulative_share", sorter:"number",
                topCalc:"sum", topCalcParams:{
                    precision:2,
                },
                sorter:"number",formatter:"number",formatterParams:{
                    decimal:".",
                    thousand:".",
                    symbol:"#",
                    
                    precision:2,
                }
            },
            ]
           },
        ],
        data:res
    })
    // $("#download-xlsx").on("click", function(){
    //     savint_table.download("xlsx", "data.xlsx", {sheetName:"My Data"});
    // });
    
    // //trigger download of data.pdf file
    // $("#download-pdf").on("click", function(){
    //     savint_table.download("pdf", "data.pdf", {
    //         orientation:"lanscape", //set page orientation to portrait
    //         title:" Report", //add title to report
    //     });
    // });
    
    })
    
    
   
    
}



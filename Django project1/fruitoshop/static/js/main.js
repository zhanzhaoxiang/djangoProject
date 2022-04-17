//用ajax刷新商品表
$(document).ready(function () {
    $('.type_class').click(function () {
        var tid = $(this).attr('tag')
        var csrf = $("input[name='csrfmiddlewaretoken']").val()
        $.post("/type_search/", {tid: tid, csrfmiddlewaretoken: csrf},
            function (data) {
                var show_type = data.show_type
                var tb = document.getElementById('tb')
                $('#type-show tr:not(:first)').empty()
                var str = ''
                for (var i = 0; i < show_type.length; i++) {
                    str += '<tr>';
                    str += '<td>' + (i + 1) + '</td>'
                    for (var j in show_type[i]) {
                        if (j === 'name') {
                            str += "<td id='detail'>"
                            str += "<a herf='https://www.baidu.com/'>" + show_type[i][j] + "</a>"
                            str += '</td>'
                        } else str += '<td>' + (show_type[i][j]) + '</td>'
                    }
                    str += '</tr>'
                }
                tb.innerHTML = str
            })
    })
})

//删除用户
$(document).ready(function () {
    $('.del').click(function () {
        var flag = window.confirm("确认是否删除！")
        if (flag) {
            // 返回值为true删除直接写url,在html可以写反向解析
            //获取删除的对象id
            var id = $(this).attr('tag')
            window.location.href = '/delete/?id=' + id
        }

    })
})

//删除商品
$(document).ready(function () {
    $('.dele').click(function () {
        var flag = window.confirm("确认是否删除！")
        if (flag) {
            // 返回值为true删除直接写url,在html可以写反向解析
            //获取删除的对象id
            var id = $(this).attr('tag')
            window.location.href = '/delete_goods/?id=' + id
        }

    })
})

//更新用户信息
$(document).ready(function () {
    $('#btn_update').click(function () {
        //获取文本框的值
        var csrf = $("input[name='csrfmiddlewaretoken']").val()
        var id = $('#uid').val()
        var username = $('#username').val()
        var phone = $('#phone').val()
        var email = $('#email').val()
        var realname = $('#realname').val()
        var address = $('#address').val()
        var age = $('#age').val()
        var job = $('#job').val()
        var gender = $('#gender').val()
        var password = $('#password').val()
        var is_not = $('#is_delete').prop('checked')
        var is_delete = 0
        if (is_not) {
            is_delete = 1
        }
        $.post("/update/", {
                id: id, username: username, phone: phone,
                email: email, realname: realname, address: address,
                age: age, job: job, gender: gender, password: password,
                is_delete: is_delete, csrfmiddlewaretoken: csrf
            },
            function (data) {
                if (data.msg === '修改成功！')
                    alert('修改成功！')
                location.href = '/show/'
            })
    })
})

//收藏商品
$(document).ready(function () {
    $('#goods_collect').click(function () {
        $this = $(this)
        clas = $this.attr('class')
        new_clas = ''
        new_d = ''
        var flag = ''
        if (clas === "bi bi-suit-heart") {
            flag = '0'//0表示未收藏，1表示已收藏
            new_clas = "bi bi-suit-heart-fill"
            new_d = 'M4 1c2.21 0 4 1.755 4 3.92C8 2.755 9.79 1 12 1s4 1.755 4 3.92c0 3.263-3.234 4.414-7.608 9.608a.513.513 0 0 1-.784 0C3.234 9.334 0 8.183 0 4.92 0 2.755 1.79 1 4 1z'
        } else if (clas === 'bi bi-suit-heart-fill') {
            flag = '1'
            new_clas = 'bi bi-suit-heart'
            new_d = 'm8 6.236-.894-1.789c-.222-.443-.607-1.08-1.152-1.595C5.418 2.345 4.776 2 4 2 2.324 2 1 3.326 1 4.92c0 1.211.554 2.066 1.868 3.37.337.334.721.695 1.146 1.093C5.122 10.423 6.5 11.717 8 13.447c1.5-1.73 2.878-3.024 3.986-4.064.425-.398.81-.76 1.146-1.093C14.446 6.986 15 6.131 15 4.92 15 3.326 13.676 2 12 2c-.777 0-1.418.345-1.954.852-.545.515-.93 1.152-1.152 1.595L8 6.236zm.392 8.292a.513.513 0 0 1-.784 0c-1.601-1.902-3.05-3.262-4.243-4.381C1.3 8.208 0 6.989 0 4.92 0 2.755 1.79 1 4 1c1.6 0 2.719 1.05 3.404 2.008.26.365.458.716.596.992a7.55 7.55 0 0 1 .596-.992C9.281 2.049 10.4 1 12 1c2.21 0 4 1.755 4 3.92 0 2.069-1.3 3.288-3.365 5.227-1.193 1.12-2.642 2.48-4.243 4.38z'
        }
        $.getJSON('/goods_collection/', {"id": $('#goods_collect').attr('tag'), 'flag': flag}, function (data) {
            if (data.msg === '取消收藏成功！' || data.msg === '收藏成功！') {
                alert(data.msg)
                $this.prev().text(data.save_num)
                $this.attr('class', new_clas)
                $("#img_path").attr('d', new_d)

            } else if (data.msg === '取消收藏失败！' || data.msg === '收藏失败！') {
                alert(data.msg)
            }
        })
    })
})

// 在商品详情页面根据某个商品的价格数量计算总价
//绑定做法
// $(document).ready(function () {
//     $('#add').click(function() {
//        var num =parseInt($('#goods_num').val());
//         num+=1;
//         //设置数量
//         $('#goods_num').val(num);
//         //第一个em标签获得单价
//        var price =parseFloat($("em").first().text());
//
//         var total = num*price;
//         //第二个em标签设置总价
//         $("em").last().text(total)
//     })
// })
// 不绑定
function calculateTotal(flag) {

    var num = parseInt($('#goods_num').val());

    if (flag === '+') {
        num += 1;
    } else if (flag === '-') {
        if (num === 1) {
            alert('只能整件！')
            return
        }
        num -= 1;
    }
    //设置数量
    $('#goods_num').val(num);
    //第一个em标签获得单价
    var price = parseFloat($("em").first().text());

    var total = (num * price).toFixed(2);
    //第二个em标签设置总价
    $("em").last().text(total)
}

//加入购物车
$(document).ready(function () {
    $('#cart_add').click(function () {
        $.getJSON('/cart_add/', {
            'id': $('#cart_add').attr('tag'),
            'goodsnum': $('#goods_num').val(),
            'total': $("em").last().text()
        }, function (data) {
            if (data.status === '添加成功！') {
                $('#my_cart_number').html(data.count)
            } else if (data.status === '添加失败！') {
                alert(data.status)
            } else if (data.status === '400') {
                location.href = '/user_login/'
            }
        })
    })
})

//浏览购物车
$(document).ready(function () {
    $('#my_cart').click(function () {
        location.href = '/show_my_cart/'
    })
})

//购物车商品选中
$(document).ready(function () {
    $('.selected').click(function () {
        var all_total = parseFloat(document.getElementById('all_total_child').innerText);
        var gnum = parseFloat(document.getElementById('gnum_child').innerText)
        var ischecked = $(this).prop('checked')
        var all_gum = document.getElementsByClassName('selected').length
        //找某个标签的父标签和子标签
        var single_total = $(this).parent().parent().children('.single_total').children().text()
        if (ischecked) {
            gnum += 1
            all_total += parseFloat(single_total)
            $(this).attr('name', 'selected_1')
        } else {
            $('#all_selected').prop('checked', false)
            gnum -= 1
            all_total -= parseFloat(single_total)
            $(this).attr('name', 'selected_0')
        }
        if (gnum === all_gum) {
            $('#all_selected').prop('checked', true)
        }
        $('#all_total').children().text(all_total.toFixed(2))
        $('#gnum').children().text(gnum)
    })

//购物车全选
    $('#all_selected').click(function () {
        var all_total = 0
        var gnum = 0
        var ischecked = $(this).prop('checked')
        if (ischecked) {
            $('.selected').each(function () {
                $(this).prop('checked', true)
                $(this).attr('name', 'selected_1')
                all_total += parseFloat($(this).parent().parent().children('.single_total').children().text())
                gnum += 1
            })
        } else {
            $('.selected').each(function () {
                $(this).prop('checked', false)
                $(this).attr('name', 'selected_0')
                all_total = 0
                gnum = 0
            })
        }
        $('#all_total').children().text(all_total.toFixed(2))
        $('#gnum').children().text(gnum)
    })
})

//对购物车内某个商品数量改变
$(document).ready(function () {
    $('.minus').click(function () {
        var num = parseInt($(this).next('.goods_num').val());
        var primary_num = num;
        //第一个em标签获得单价
        var price = parseFloat($(this).parent().parent().children('.single_price').children().text());

        if (num === 1) {
            alert('只能整件！');
            return;
        } else {
            num -= 1;
            //设置数量
            $(this).next().val(num);

            var total = num * price;
            //第二个em标签设置总价
            $(this).parent().parent().children('.single_total').children().text(total.toFixed(2));

            var gid = $(this).next('.goods_num').attr('tag');

            var ischecked = $(this).parent().parent().children('.father_selected').children('.selected').prop('checked');
            var all_total = parseFloat($('#all_total').children().text());
            var temporary_total = all_total - primary_num * price;
            if (ischecked) {
                all_total = temporary_total + total;
            }
            $('#all_total').children().text(all_total.toFixed(2));
            $.getJSON('/cart_goods_adjust/', {'gid': gid, 'num': num, 'total': total})

        }

    })
    $('.add').click(function () {
        var num = parseInt($(this).prev('.goods_num').val());
        var primary_num = num
        num += 1;
        //设置数量
        $(this).prev().val(num)
        //第一个em标签获得单价
        var price = parseFloat($(this).parent().parent().children('.single_price').children().text());

        var total = num * price;
        //第二个em标签设置总价
        $(this).parent().parent().children('.single_total').children().text(total.toFixed(2))

        var gid = $(this).prev('.goods_num').attr('tag');
        var ischecked = $(this).parent().parent().children('.father_selected').children('.selected').prop('checked')
        var all_total = parseFloat($('#all_total').children().text())
        var temporary_total = all_total - primary_num * price
        if (ischecked) {
            all_total = temporary_total + total
        }
        $('#all_total').children().text(all_total.toFixed(2))
        $.getJSON('/cart_goods_adjust/', {'gid': gid, 'num': num, 'total': total})
    })

})

//删除购物车商品
$(document).ready(function () {
    $('.cart_del').click(function () {
        var flag = window.confirm("确认是否删除该商品！")
        if (flag) {
            // 返回值为true删除直接写url,在html可以写反向解析
            //获取删除的对象id
            var id = $(this).attr('tag')
            window.location.href = '/cart_del/?gid=' + id
        }

    })
})


# Kpi Procedures Class
def get_kpis():
    return """
        with c_reg_users as (
            select id id_date, userlist->'rtc_online_users'->'reg_users' users
            from rtc_online_users rou
            where id between '2022-10-01'::date and '2022-10-31'::date
                and json_array_length(userlist->'rtc_online_users'->'reg_users') > 0
        ),
        all_users as (
            select x.* from c_reg_users a
            left join lateral json_to_recordset(a.users::json) x (id int, r_id varchar) on true
        ),
        more_one_visits as (
            select r_id from all_users group by r_id having count(r_id) > 1
        )
        select more_one_visits from (select count(r_id) more_one_visits from more_one_visits) tmp
    """
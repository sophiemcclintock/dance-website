/* database creation script */

drop table if exists news;
drop table if exists member;

/* create table */

create table member(
    member_id integer primary key autoincrement not null,
    name text not null,
    email text not null unique,
    password text not null,
    authorisation integer not null
);

create table news(
    news_id integer primary key autoincrement not null,
    title text not null unique,
    subtitle text not null unique,
    content text not null unique,
    newsdate date not null,
    member_id integer not null,
    foreign key(member_id) references member(member_id)
);

insert into member (name, email, password, authorisation)
values ('Sophie', 'sophiecatemcclintock@gmail.com', 'temp', 0);
insert into member (name, email, password, authorisation)
values ('Molly', 'mollyroseschaefer@gmail.com', 'temp', 0);
insert into member (name, email, password, authorisation)
values ('Eva', 'eva.wgtn@gmail.com', 'temp', 1);
insert into member (name, email, password, authorisation)
values ('Adia', 'adiajanice@gmail.com', 'temp', 1);

insert into news(title, subtitle, content, newsdate, member_id)
values ('Hip Hop Unite Competition',
        'From Friday 9th to Saturday 10th of June',
        'Our hip hop dance crew are competing in this very high level competition, and we are all very excited. It would be awesome if as many people as possible could come and cheer us on!',
        '2023-03-04 11:40:00',
        (select member_id from member where name = "Sophie")
        );

values ('Dance Class with Kezia Shepherd',
        'On the 10th of August',
        'Kezia is an ex-Riptide dancer who has gone on to university in Christchurch but she still loves to teach whenever she can. Her classes are ballet and she does beginner, intermediate and advanced lessons. At 2pm will be the beginners lesson, the intermediate lesson will be at 3pm and the advanced lesson at 4pm. Please come along!' ,
        '2023-03-04 12:02:00',
        (select member_id from member where name = "Molly")
        );


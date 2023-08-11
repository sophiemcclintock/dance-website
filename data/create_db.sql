/* database creation script */

drop table if exists news;
drop table if exists member;
drop table if exists classes;
drop table if exists registration;
drop table if exists contact;

/* create table */

create table member(
    member_id integer primary key autoincrement not null,
    name text not null unique,
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

create table classes(
    classes_id integer primary key autoincrement not null,
    classes_title text not null,
    content text not null unique,
    image not null,
    member_id integer not null,
    foreign key(member_id) references member(member_id)
);

insert into classes(classes_title, content, image, member_id)
values ('JAZZ',
        'Our jazz class is taught by ex-Riptide pupil Eva Tunnicliffe. It is an upbeat, stylised, technical dance style. You will be building strength and coordination to assist with jumps, turns and flexibility. Get grooving to fresh music and new choreography. Our classes cater for all ages, whether you are Year 9 or Year 13, we would love to have you!',
        'eva_leg_stretch.jpg',
        '1');

insert into classes(classes_title, content, image, member_id)
values ('CONTEMPORARY',
        'Contemporary is an expressive style that combines elements of jazz, lyrical and ballet. You will be striving to connect the mind and body to move around the space with intention and control. You will learn how to flow your movements togather with alignment and technique. Again, our contemporary classes cater for all students.',
        'startled_rabbits.jpg',
        '2');

insert into classes(classes_title, content, image, member_id)
values ('TAP',
        'Tap is characterised by the creation of musically-focused rhythm performance using tap shoes striking on the floor in accordance with the music. It is difficult to master but once you get it, it is very satisfying! Tap shoes are required, we have some you can buy but you must have your own shoes. Tap is only for Year 12 and 13, but exceptions may be given.',
        'eva_front_on.jpg',
        '1');

insert into classes(classes_title, content, image, member_id)
values ('HIP HOP',
        'Hip Hop is a style of dance very different from the other styles we offer. It is a fierce, dynamic, funky style of dance that encourages bold moves and confidence. This high energy style is paired with fresh beats creating a vibrant environment to move and groove. We offer classes for everyone and we really promote the community that grows within these classes.',
        'hip_hop.jpg',
        '3');

create table registration(
    member_id integer not null,
    classes_id integer not null,
    foreign key(classes_id) references classes(classes_id),
    foreign key(member_id) references member(member_id),
    primary key (member_id, classes_id)
);

insert into news(title, subtitle, content, newsdate, member_id)
values ('HIP HOP UNITE DANCE COMPETITION',
        'From Friday 9th to Saturday 10th of June',
        'Our hip hop dance crew are competing in this very high level competition, and we are all very excited. It would be awesome if as many people as possible could come and cheer us on!',
        datetime('now'),
        '1');

insert into news(title, subtitle, content, newsdate, member_id)
values ('DANCE CLASS WITH KEZIA SHEPHERD',
        'On the 10th of August',
        'Kezia is an ex-Riptide dancer who has gone on to university in Christchurch but she still loves to teach whenever she can. Her classes are ballet and she does beginner, intermediate and advanced lessons. At 2pm will be the beginners lesson, the intermediate lesson will be at 3pm and the advanced lesson at 4pm. Please come along!' ,
        datetime('now'),
        '1');

create table contact(
    contact_id integer primary key autoincrement not null,
    contact_name text not null,
    email text not null unique,
    message not null
);

insert into contact(contact_name, email, message, newsdate)
values ('Eva McClintock',
        'evagracemcclintock@gmaail.com',
        'I would like to know what is the easiest class to start with for someone who has never danced before',
        datetime('now'))

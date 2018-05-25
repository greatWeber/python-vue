drop database if exists blog;

create database blog;

use blog;

grant select, insert, update, delete on blog.* to 'root'@'localhost' identified by 'root';

create table users (
    `id` varchar(60) not null,
    `email` varchar(50) not null,
    `password` varchar(50) not null,
    `is_admin` bool not null,
    `is_del` bool not null,
    `name` varchar(50) not null,
    `nickname` varchar(50) not null,
    `image` varchar(500) not null,
    `created_time` real not null,
    key `idx_created_time` (`created_time`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table blogs (
    `id` varchar(60) not null,
    `user_id` varchar(60) not null,
    `user_name` varchar(50) not null,
    `user_image` varchar(500) not null,
    `thumb` varchar(500) not null,
    `title` varchar(50) not null,
    `info` varchar(200) not null,
    `content` mediumtext not null,
    `created_time` real not null,
    `is_del` bool not null,
    key `idx_created_time` (`created_time`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table comments (
    `id` varchar(60) not null,
    `blog_id` varchar(60) not null,
    `user_id` varchar(60) not null,
    `user_name` varchar(50) not null,
    `user_image` varchar(500) not null,
    `content` mediumtext not null,
    `created_time` real not null,
    `is_del` bool not null,
    key `idx_created_time` (`created_time`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table tokens (
    `id` varchar(60) not null,
    `uid` varchar(60) not null,
    `token_key` varchar(100) not null,
    `last_time` real not null,
    primary key (`id`)
) engine=innodb default charset=utf8;
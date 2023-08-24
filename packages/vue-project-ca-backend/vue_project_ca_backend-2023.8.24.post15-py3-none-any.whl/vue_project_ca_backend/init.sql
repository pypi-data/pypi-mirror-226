-- 数据状态
INSERT INTO "states" ("id", "name", "langname") VALUES ('1', 'valid', '有效');
INSERT INTO "states" ("id", "name", "langname") VALUES ('2', 'freeze', '冻结');
INSERT INTO "states" ("id", "name", "langname") VALUES ('3', 'delete', '删除');
-- 系统基础角色
INSERT INTO roles (id, name, langname, state) VALUES (1, 'super admin', '超级管理员', 1);
INSERT INTO roles (id, name, langname, state) VALUES (2, 'admin', '管理员', 1);
INSERT INTO roles (id, name, langname, state) VALUES (3, 'user', '用户', 1);

migration_postgres_create = {
    "appr_header" : 
        '''
            CREATE TABLE "USR_ISMG"."APPR_HEADER" (
                "DOCUNO" VARCHAR PRIMARY KEY,
                "MHT_SOURCE" TEXT NULL,
                "FILE_NAME" VARCHAR NULL,
                "TITLE" VARCHAR NULL,
                "TYPE" VARCHAR NULL,
                "FORMCODE" VARCHAR NULL,
                "FORMNAME" VARCHAR NULL,
                "DRAFTERNO" VARCHAR NULL,
                "DRAFTER" VARCHAR NULL,
                "DRAFTERGROUPNO" VARCHAR NULL,
                "DRAFTGROUPNAME" VARCHAR NULL,
                "DRAFTDAY" VARCHAR NULL,
                "APRVDAY" VARCHAR NULL,
                "EXPIREDAY" VARCHAR NULL,
                "PUBLIC" VARCHAR NULL,
                "STEP" VARCHAR NULL,
                "EXTRADATA" VARCHAR NULL
            )
        ''',
    "appr_line" :
        '''
            CREATE TABLE "USR_ISMG"."APPR_LINE" (
                "DOCUNO" VARCHAR NULL,
                "USERNO" VARCHAR NULL,
                "USERNAME" VARCHAR NULL,
                "GROUPNO" VARCHAR NULL,
                "GROUPNAME" VARCHAR NULL,
                "POSITION" VARCHAR NULL,
                "DUTY" VARCHAR NULL,
                "ORDER" VARCHAR NULL,
                "SEQ" VARCHAR NULL,
                "METHOD" VARCHAR NULL,
                "DATE" VARCHAR NULL,
                "RESULT" VARCHAR NULL
            )
        ''',
    "appr_refer" : 
        '''
            CREATE TABLE "USR_ISMG"."APPR_REFER" (
                "DOCUNO" VARCHAR NULL,
                "USERNO" VARCHAR NULL,
                "USERNAME" VARCHAR NULL,
                "GROUPNO" VARCHAR NULL,
                "GROUPNAME" VARCHAR NULL
            )
        ''',
    "appr_view" :
        '''
            CREATE TABLE "USR_ISMG"."APPR_VIEW" (
                "DOCUNO" VARCHAR NULL,
                "USERNO" VARCHAR NULL,
                "USERNAME" VARCHAR NULL,
                "GROUPNO" VARCHAR NULL,
                "GROUPNAME" VARCHAR NULL
            )
        ''',
    "appr_file" : 
        '''
            CREATE TABLE "USR_ISMG"."APPR_FILE" (
                "DOCUNO" VARCHAR NULL,
                "FILENAME" VARCHAR NULL,
                "PATH" VARCHAR NULL,
                "FLAG" VARCHAR NULL,
                "SEQ" INT4 NULL,
                "FILE_CHECK" CHAR(1) NULL
            )
        '''
}

migration_create = {
    "appr_header" : 
        '''
            CREATE TABLE "USR_ISMG"."APPR_HEADER" (
                "DOCUNO" VARCHAR2(100) PRIMARY KEY,
                "MHT_SOURCE" LONG NULL,
                "FILE_NAME" VARCHAR2(4000) NULL,
                "TITLE" VARCHAR2(4000) NULL,
                "TYPE" VARCHAR2(4000) NULL,
                "FORMCODE" VARCHAR2(4000) NULL,
                "FORMNAME" VARCHAR2(4000) NULL,
                "DRAFTERNO" VARCHAR2(4000) NULL,
                "DRAFTER" VARCHAR2(4000) NULL,
                "DRAFTERGROUPNO" VARCHAR2(4000) NULL,
                "DRAFTGROUPNAME" VARCHAR2(4000) NULL,
                "DRAFTDAY" VARCHAR2(4000) NULL,
                "APRVDAY" VARCHAR2(4000) NULL,
                "EXPIREDAY" VARCHAR2(4000) NULL,
                "PUBLIC" VARCHAR2(4000) NULL,
                "STEP" VARCHAR2(4000) NULL,
                "EXTRADATA" VARCHAR2(4000) NULL
            )
        ''',
    "appr_line" :
        '''
            CREATE TABLE "USR_ISMG"."APPR_LINE" (
                "DOCUNO" VARCHAR2(100) NULL,
                "USERNO" VARCHAR2(4000) NULL,
                "USERNAME" VARCHAR2(4000) NULL,
                "GROUPNO" VARCHAR2(4000) NULL,
                "GROUPNAME" VARCHAR2(4000) NULL,
                "POSITION" VARCHAR2(4000) NULL,
                "DUTY" VARCHAR2(4000) NULL,
                "ORDER" VARCHAR2(4000) NULL,
                "SEQ" VARCHAR2(4000) NULL,
                "METHOD" VARCHAR2(4000) NULL,
                "DATE" VARCHAR2(4000) NULL,
                "RESULT" VARCHAR2(4000) NULL
            )
        ''',
    "appr_refer" : 
        '''
            CREATE TABLE "USR_ISMG"."APPR_REFER" (
                "DOCUNO" VARCHAR2(100) NULL,
                "USERNO" VARCHAR2(4000) NULL,
                "USERNAME" VARCHAR2(4000) NULL,
                "GROUPNO" VARCHAR2(4000) NULL,
                "GROUPNAME" VARCHAR2(4000) NULL
            )
        ''',
    "appr_view" :
        '''
            CREATE TABLE "USR_ISMG"."APPR_VIEW" (
                "DOCUNO" VARCHAR2(100) NULL,
                "USERNO" VARCHAR2(4000) NULL,
                "USERNAME" VARCHAR2(4000) NULL,
                "GROUPNO" VARCHAR2(4000) NULL,
                "GROUPNAME" VARCHAR2(4000) NULL
            )
        ''',
    "appr_file" : 
        '''
            CREATE TABLE "USR_ISMG"."APPR_FILE" (
                "DOCUNO" VARCHAR2(100) NULL,
                "FILENAME" VARCHAR2(4000) NULL,
                "PATH" VARCHAR2(4000) NULL,
                "FLAG" VARCHAR2(100) NULL,
                "SEQ" INTEGER NULL,
                "FILE_CHECK" CHAR(1) NULL
            )
        '''
}

migration_truncate = {
    "appr_header" : 
        '''
            truncate table "USR_ISMG"."APPR_HEADER"
        ''',
    "appr_line" :
        '''
            truncate table "USR_ISMG"."APPR_LINE"
        ''',
    "appr_refer" : 
        '''
            truncate table "USR_ISMG"."APPR_REFER"
        ''',
    "appr_view" :
        '''
            truncate table "USR_ISMG"."APPR_VIEW"
        ''',
    "appr_file" : 
        '''
            truncate table "USR_ISMG"."APPR_FILE"
        '''
}

migration_insert = {
    "appr_header" : 
        '''
            INSERT INTO "USR_ISMG"."APPR_HEADER" ("FILE_NAME", "MHT_SOURCE", "TITLE", "TYPE", "FORMCODE", "FORMNAME", "DOCUNO", 
            "DRAFTERNO", "DRAFTER", "DRAFTERGROUPNO", "DRAFTGROUPNAME", "DRAFTDAY", "APRVDAY", "EXPIREDAY", "PUBLIC", "STEP", "EXTRADATA") 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
    "appr_line" :
        '''
            INSERT INTO "USR_ISMG"."APPR_LINE" ("DOCUNO", "USERNO", "USERNAME", "GROUPNO", "GROUPNAME", "POSITION", "DUTY", 
            "ORDER", "SEQ", "METHOD", "DATE", "RESULT") 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
    "appr_refer" : 
        '''
            INSERT INTO "USR_ISMG"."APPR_REFER" ("DOCUNO", "USERNO", "USERNAME", "GROUPNO", "GROUPNAME") 
            VALUES (?, ?, ?, ?, ?)
        ''',
    "appr_view" :
        '''
            INSERT INTO "USR_ISMG"."APPR_VIEW" ("DOCUNO", "USERNO", "USERNAME", "GROUPNO", "GROUPNAME") 
            VALUES (?, ?, ?, ?, ?)
        ''',
    "appr_file" : 
        '''
            INSERT INTO "USR_ISMG"."APPR_FILE" ("DOCUNO", "FILENAME", "PATH", "SEQ", "FILE_CHECK") 
            VALUES (?, ?, ?, ?, ?)
        '''
}

read_data = {
    "appr_file" : 
        '''
            SELECT "DOCUNO", "PATH", "FLAG", "SEQ" FROM "USR_ISMG"."APPR_FILE" 
            WHERE "FLAG" IS NULL
            AND FILE_CHECK = 'Y'
            AND SEQ BETWEEN ? AND ?
        ''',
    "appr_file_delete" : 
        '''
            SELECT "DOCUNO", "PATH", "FLAG", "SEQ" FROM "USR_ISMG"."APPR_FILE" 
            WHERE "FLAG" = 'success'
            AND FILE_CHECK = 'Y'
            AND SEQ BETWEEN ? AND ?
        '''
}

update_data = {
    "appr_file" : 
        '''
            UPDATE "USR_ISMG"."APPR_FILE" SET FLAG='' WHERE "DOCUNO" = ?
        '''
}
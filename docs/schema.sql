-- =====================================================================
--  Book Shelf — schema de referencia
--
--  ISTO E DOCUMENTACAO, NAO E PARA EXECUTAR.
--
--  Quem cria as tabelas de verdade e a migration do Alembic
--  (`flask db upgrade`). Este arquivo existe para estudar o modelo,
--  revisar em PR e usar na apresentacao.
--
--  NAO copie este arquivo para `infra/mysql/init/`. Aquela pasta e
--  executada pelo MySQL na primeira subida do container, e o resultado
--  seria o banco com as tabelas ja criadas por fora do Alembic — o
--  `flask db upgrade` iria falhar dizendo que a tabela ja existe.
--
--  Gerado a partir de backend/app/models/ e conferido contra um banco
--  real. Se mexer nos models, atualize aqui no mesmo PR.
-- =====================================================================

-- O banco `bookshelf` ja e criado pelo docker-compose.yml da raiz.
USE bookshelf;


-- =====================================================================
-- 1) USUARIOS                                                    [AC1]
-- =====================================================================

CREATE TABLE users (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  username      VARCHAR(30)     NOT NULL,
  email         VARCHAR(255)    NOT NULL,
  password_hash VARCHAR(255)    NOT NULL,  -- hash, nunca a senha
  display_name  VARCHAR(80)     NULL,
  bio           VARCHAR(500)    NULL,
  avatar_url    VARCHAR(500)    NULL,
  role          ENUM('user','admin') NOT NULL DEFAULT 'user',
  is_active     BOOLEAN         NOT NULL DEFAULT TRUE,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP
                                ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_users_username (username),
  UNIQUE KEY uq_users_email    (email)
) ENGINE=InnoDB;


-- =====================================================================
-- 2) CATALOGO                                                    [AC1]
-- =====================================================================

CREATE TABLE works (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  type           ENUM('book','movie') NOT NULL DEFAULT 'book',
  title          VARCHAR(255)    NOT NULL,
  original_title VARCHAR(255)    NULL,
  slug           VARCHAR(280)    NOT NULL,   -- ex.: "duna-1965", vai na URL
  release_year   SMALLINT UNSIGNED NULL,
  synopsis       TEXT            NULL,
  cover_url      VARCHAR(500)    NULL,
  created_by     BIGINT UNSIGNED NOT NULL,
  created_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP
                                 ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_works_slug (slug),
  KEY idx_works_type_year  (type, release_year),
  KEY idx_works_title      (title),
  CONSTRAINT fk_works_created_by
    FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE RESTRICT,
  CONSTRAINT ck_works_year
    CHECK (release_year IS NULL OR release_year BETWEEN 1400 AND 2200)
) ENGINE=InnoDB;


CREATE TABLE book_details (
  work_id    BIGINT UNSIGNED NOT NULL,
  isbn13     CHAR(13)        NULL,
  publisher  VARCHAR(150)    NULL,
  page_count SMALLINT UNSIGNED NULL,
  language   VARCHAR(40)     NULL,
  PRIMARY KEY (work_id),
  UNIQUE KEY uq_book_isbn13 (isbn13),
  CONSTRAINT fk_book_details_work
    FOREIGN KEY (work_id) REFERENCES works (id) ON DELETE CASCADE
) ENGINE=InnoDB;


CREATE TABLE genres (
  id   SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(60) NOT NULL,
  slug VARCHAR(70) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_genres_name (name),
  UNIQUE KEY uq_genres_slug (slug)
) ENGINE=InnoDB;

CREATE TABLE work_genres (
  work_id  BIGINT UNSIGNED   NOT NULL,
  genre_id SMALLINT UNSIGNED NOT NULL,
  PRIMARY KEY (work_id, genre_id),
  KEY idx_work_genres_genre (genre_id),
  CONSTRAINT fk_work_genres_work
    FOREIGN KEY (work_id)  REFERENCES works (id)  ON DELETE CASCADE,
  CONSTRAINT fk_work_genres_genre
    FOREIGN KEY (genre_id) REFERENCES genres (id) ON DELETE CASCADE
) ENGINE=InnoDB;


CREATE TABLE people (
  id   BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(150) NOT NULL,
  slug VARCHAR(170) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_people_slug (slug),
  KEY idx_people_name (name)
) ENGINE=InnoDB;

CREATE TABLE work_credits (
  work_id        BIGINT UNSIGNED NOT NULL,
  person_id      BIGINT UNSIGNED NOT NULL,
  role           ENUM('author','translator','director','screenwriter','actor')
                 NOT NULL,
  character_name VARCHAR(150) NULL,
  -- `role` na PK: a mesma pessoa pode ser autora E tradutora da mesma obra.
  PRIMARY KEY (work_id, person_id, role),
  KEY idx_work_credits_person (person_id),
  CONSTRAINT fk_work_credits_work
    FOREIGN KEY (work_id)   REFERENCES works (id)  ON DELETE CASCADE,
  CONSTRAINT fk_work_credits_person
    FOREIGN KEY (person_id) REFERENCES people (id) ON DELETE CASCADE
) ENGINE=InnoDB;


-- =====================================================================
-- 3) AVALIACOES                                            [AC2 e AC3]
--
--  `rating` e NULLABLE de proposito: a AC2 entrega comentario e a AC3
--  entrega nota. Se fosse NOT NULL, a AC2 nao teria como gravar.
--  O segundo CHECK garante que pelo menos um dos dois exista.
-- =====================================================================

CREATE TABLE reviews (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  user_id      BIGINT UNSIGNED NOT NULL,
  work_id      BIGINT UNSIGNED NOT NULL,
  body         TEXT            NULL,        -- [AC2]
  rating       DECIMAL(2,1)    NULL,        -- [AC3] 0.5 a 5.0, de meio em meio
  has_spoilers BOOLEAN         NOT NULL DEFAULT FALSE,
  consumed_on  DATE            NULL,
  created_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP
                               ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  -- Regra central: 1 avaliacao por usuario por obra. A segunda vez e EDICAO.
  UNIQUE KEY uq_reviews_user_work (user_id, work_id),
  KEY idx_reviews_work_created (work_id, created_at),
  CONSTRAINT fk_reviews_user
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
  CONSTRAINT fk_reviews_work
    FOREIGN KEY (work_id) REFERENCES works (id) ON DELETE CASCADE,
  CONSTRAINT ck_reviews_rating
    CHECK (rating IS NULL
           OR (rating >= 0.5 AND rating <= 5.0 AND MOD(rating * 10, 5) = 0)),
  CONSTRAINT ck_reviews_nota_ou_texto
    CHECK (rating IS NOT NULL OR body IS NOT NULL)
) ENGINE=InnoDB;


-- Thread de respostas a uma avaliacao. EXTRA — nao esta nas 4 entregas.
CREATE TABLE comments (
  id                BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  review_id         BIGINT UNSIGNED NOT NULL,
  user_id           BIGINT UNSIGNED NOT NULL,
  parent_comment_id BIGINT UNSIGNED NULL,   -- NULL = raiz; preenchido = resposta
  body              VARCHAR(2000)   NOT NULL,
  is_deleted        BOOLEAN         NOT NULL DEFAULT FALSE,  -- soft delete
  created_at        TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at        TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP
                                    ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_comments_review (review_id, created_at),
  -- Sem KEY em user_id: o MySQL ja cria um indice para a FK. Um indice
  -- explicito duplicado nao acelera nada e quebra o downgrade (erro 1553).
  CONSTRAINT fk_comments_review
    FOREIGN KEY (review_id) REFERENCES reviews (id) ON DELETE CASCADE,
  CONSTRAINT fk_comments_user
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
  CONSTRAINT fk_comments_parent
    FOREIGN KEY (parent_comment_id) REFERENCES comments (id) ON DELETE CASCADE
) ENGINE=InnoDB;


-- Curtida em avaliacao. EXTRA — nao esta nas 4 entregas.
CREATE TABLE review_likes (
  user_id    BIGINT UNSIGNED NOT NULL,
  review_id  BIGINT UNSIGNED NOT NULL,
  created_at TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, review_id),   -- impede curtir duas vezes
  KEY idx_review_likes_review (review_id),
  CONSTRAINT fk_review_likes_user
    FOREIGN KEY (user_id)   REFERENCES users (id)   ON DELETE CASCADE,
  CONSTRAINT fk_review_likes_review
    FOREIGN KEY (review_id) REFERENCES reviews (id) ON DELETE CASCADE
) ENGINE=InnoDB;


-- =====================================================================
-- 4) FAVORITOS                                        [Entrega final]
-- =====================================================================

CREATE TABLE favorites (
  user_id    BIGINT UNSIGNED NOT NULL,
  work_id    BIGINT UNSIGNED NOT NULL,
  created_at TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  -- A PK composta e o que impede favoritar o mesmo livro duas vezes.
  -- Nao precisa de coluna `id` nem de validacao no codigo.
  PRIMARY KEY (user_id, work_id),
  CONSTRAINT fk_favorites_user
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
  CONSTRAINT fk_favorites_work
    FOREIGN KEY (work_id) REFERENCES works (id) ON DELETE CASCADE
) ENGINE=InnoDB;

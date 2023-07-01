--EditTimeplan
-- Create model AdminUser
--
CREATE TABLE `admin` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `nom` varchar(100) NOT NULL, `prenom` varchar(100) NOT NULL, `email` varchar(254) NOT NULL UNIQUE, `numero_telephone` varchar(20) NOT NULL, `mot_de_passe` varchar(128) NOT NULL, `promotion` varchar(2) NOT NULL, `Code_confirmation` integer NULL);
--
-- Create model CoursProgrammer
--
CREATE TABLE `coursProgrammer` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `jour` varchar(100) NOT NULL, `promotion` varchar(128) NOT NULL, `heure_debut` time(6) NOT NULL, `heure_fin` time(6) NOT NULL, `matiere` varchar(150) NOT NULL, `salle` varchar(150) NOT NULL, `teacher` varchar(128) NOT NULL);
--
-- Create model Matiere
--
CREATE TABLE `Matiere` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `nom` varchar(100) NOT NULL, `enseignant` varchar(128) NOT NULL, `timing` integer NOT NULL, `Informations` varchar(500) NOT NULL, `promotion` varchar(28) NOT NULL);
--
-- Create model Promotion
--
CREATE TABLE `Promotion` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `nom` varchar(100) NOT NULL, `annee` varchar(2) NOT NULL, `groupe` varchar(2) NULL);
--
-- Create model Salle
--
CREATE TABLE `Salle` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `nom` varchar(100) NOT NULL);
--
-- Create model CoursProgrammerL1
--
CREATE TABLE `coursProgrammerL1` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `Date` varchar(128) NOT NULL, `jour` varchar(128) NOT NULL, `promotion` varchar(128) NOT NULL, `heure_debut` varchar(150) NOT NULL, `heure_fin` varchar(150) NOT NULL, `salle` varchar(150) NOT NULL, `teacher` varchar(128) NOT NULL, `groupe` varchar(128) NOT NULL, `matiere_id` bigint NOT NULL);
ALTER TABLE `coursProgrammerL1` ADD CONSTRAINT `coursProgrammerL1_matiere_id_950580fe_fk_Matiere_id` FOREIGN KEY (`matiere_id`) REFERENCES `Matiere` (`id`);

--showtimeplan
-- Create model User
--
CREATE TABLE `etudiants_enregistres` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `nom` varchar(120) NOT NULL, `prenom` varchar(120) NOT NULL, `email` varchar(254) NOT NULL UNIQUE, `numero_telephone` varchar(20) NOT NULL, `mot_de_passe` varchar(128) NOT NULL, `code_de_confirmation` integer NULL);
--
-- Create model CoursProgrammerL1Etu
--
CREATE TABLE `coursProgrammerL1Etu` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `Date` varchar(128) NOT NULL, `jour` varchar(128) NOT NULL, `promotion` varchar(128) NOT NULL, `heure_debut` varchar(150) NOT NULL, `heure_fin` varchar(150) NOT NULL, `salle` varchar(150) NOT NULL, `teacher` varchar(128) NOT NULL, `groupe` varchar(128) NOT NULL, `matiere_id` bigint NOT NULL);
ALTER TABLE `coursProgrammerL1Etu` ADD CONSTRAINT `coursProgrammerL1Etu_matiere_id_cbfda821_fk_Matiere_id` FOREIGN KEY (`matiere_id`) REFERENCES `Matiere` (`id`);

"""
One To Many, is used to mark that an instance of a class can be associated with many instances of another class.
For example, on a blog engine, an instance of the Article class could be associated with
 many instances of the Comment class

http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html
A one to many relationship places a foreign key on the child table referencing the parent.
relationship() is then specified on the parent, as referencing a collection of items represented by the child:

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship("Child")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))

To establish a bidirectional relationship in one-to-many, where the reverse side is a many to one,
 specify an additional relationship() and connect the two using the relationship.back_populates parameter:

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship("Child", back_populates="parent")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    parent = relationship("Parent", back_populates="children")

"""

from sqlalchemy import create_engine, Column, Integer, ForeignKey, BLOB, String
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

Engine = create_engine("sqlite:///dbs//one_to_many_exp.db")
Session = scoped_session(sessionmaker(bind=Engine, autocommit=True, autoflush=True))
Base = declarative_base()


class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    comments = relationship("Comment")   # Here we pass the class name

    def __init__(self, title):
        self.title = title

    def __str__(self):
        com = [comment.comment for comment in self.comments]
        return "Article: {0} comments: {1}".format(self.title, ", ".join(com))


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    comment = Column(String)
    article_id = Column(Integer, ForeignKey('articles.id')) # here we pass the table name

    def __init__(self, article_id, comment):
        self.article_id = article_id
        self.comment = comment

    def __str__(self):
        return "Comment: {0} on Article: {1}".format(self.comment, self.article_id)

# Note: whenever change in table/class, delete the existing dbs

if __name__ == '__main__':
  Base.metadata.create_all(Engine)
  a1 = Article('Array Replication')
  a2 = Article('Host Replication')
  Session.add(a1)
  Session.add(a2)
  arr_rep_art = Session.query(Article).filter(Article.title == 'Array Replication').first()
  host_rep_art = Session.query(Article).filter(Article.title == 'Host Replication').first()
  comment1 = Comment(arr_rep_art.id, 'Nice')
  Session.add(comment1)
  comment2 = Comment(arr_rep_art.id, 'Good')
  Session.add(comment2)

  arr_rep_art = Session.query(Article).filter(Article.title == 'Array Replication').first()
  print (arr_rep_art)
  print ('Saved Successfully')
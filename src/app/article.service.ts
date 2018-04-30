import { Injectable } from '@angular/core';

@Injectable()
export class ArticleService {

  constructor() { }

  getNumber(): number {
    return 5;
  }

}

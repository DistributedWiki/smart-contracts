import { Component } from '@angular/core';
import {ArticleService} from './article.service';
import {Article} from './contracts/Article';
import {Web3Service} from './web3.service';
import BigNumber from 'web3/bower/bignumber.js/bignumber';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Distributed wikipedia';
  nModifications: BigNumber;


  constructor(public articleService: ArticleService,
              public article: Article,
              public web3Service: Web3Service) {

  }

  async getM() {
    this.nModifications = await this.article.nModifications;
  }

  async modify() {
    await this.article.updateTx(new BigNumber(0x1));
  }
}
